from collections import deque
from threading import Lock
from typing import List
from functools import partial

from benedict.agent import TreasonAgent
from benedict.agentWrapper import TreasonAgentWrapper

NAMES = ["benedict", "arnold"]


class TreasonGameManager:
    """
    TreasonGameManager created:
    - Agents created
    - Agents connect to server (runGames)
    - Agents connect to model manager (which spools up threads)
      - HTTP keep-alive?
      - load-balancing?
    - Agents connect to and start game
    - Agents chooses model (self-play)(tell model to update parameters)
      - games are quick, so updates to the model can wait
    - Agents play game
      - Agents pass observation back to model
      - model pass action to agent (note: careful about multple writes to single tcp connection)
      - Loop
      - Game ends
    - Manager takes room_size agents from queue
      - in onLeave callback thread (TOCTOU)
    - Selected agents connect to and start game
    - Loop
    """

    def __init__(self, *,
                 agent_count: int,
                 room_size: int,
                 game_addr: str,
                 model_addr: str = None):
        """
        - agent_count: Number of agents to manage.
        - room_size: How many agents per game
        - game_addr: Address of Treason server
        - model_addr: URL of the manager of neural networks
        """
        if room_size < 2:
            raise Exception("Invalid room size!")
        if agent_count % room_size != 0:
            raise Exception("# of Agents need to be divisble by room size!")
        self._running = False
        self._room_size = room_size
        self._game_addr = game_addr
        self._queue = AgentQueue(maxlen=agent_count)

        self._agents = [TreasonAgentWrapper(self._createAgent(name=NAMES[i % len(NAMES)] + str(i // len(NAMES)),
                                                              room_size=room_size))
                        for i in range(agent_count)]

        for agent in self._agents:
            agent.registerCallbacks(onLeaveGame=self._onAgentReady)

    def _createAgent(self, *, name: str, room_size: int) -> TreasonAgent:
        """ Override this for specific agents. """
        return TreasonAgent(name=name, k=room_size)

    def _onAgentReady(self, agent: TreasonAgentWrapper):
        self._queue.append(agent)
        room = self._queue.takeIfGeq(self._room_size)
        if room:
            lobby = partial(TreasonGameManager._onLobbyReady, room[1:])
            room[0].createGame(lobby)

    @staticmethod
    def _onLobbyReady(players: List[TreasonAgentWrapper], gameName: int):
        """ Intended for use with partials. """
        for player in players:
            player.joinGame(gameName)

    def runGames(self):
        if self._running:
            raise Exception("Already running!")

        self._running = True
        for agent in self._agents:
            agent.connect(address=self._game_addr,
                          onRegister=self._onAgentReady)


class AgentQueue:

    def __init__(self, maxlen: int = 0):
        self._queue = deque(maxlen=maxlen)
        self._lock = Lock()

    def append(self, agent: TreasonAgentWrapper):
        # Locking probably isn't needed here
        # The last last agent for a game will satisfy the size condition
        self._queue.append(agent)

    def takeIfGeq(self, size: int) -> List[TreasonAgentWrapper]:
        """
        Results a list of agents if queue length is greater or equal to size.
        Only blocks other threads running this method.
        Returns empty list if length was less than size.
        """
        result = []
        self._lock.acquire()
        try:
            if len(self._queue) >= size:
                result = [self._queue.popleft() for i in range(size)]
        finally:  # Guarantee lock release
            self._lock.release()
        return result
