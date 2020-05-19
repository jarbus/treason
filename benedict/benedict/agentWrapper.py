import socketio
from typing import Callable, Dict

from benedict.agent import TreasonAgent
from benedict.gameEnum import TreasonState
from benedict.gameState import GameState
from benedict.nnio import state_to_vector, vector_to_emission


# socketio decorators don't work with classes
class TreasonAgentWrapper:

    def __init__(self, agent: TreasonAgent):
        self.agent = agent
        self._sio = socketio.Client()
        self._playerId = None
        self._gameName = None
        self._onRegisterCallback = None
        self._onJoinGameCallback = None
        self._onCreatedGameCallback = None

        # Register listeners
        self._sio.on("handshake", handler=self._onRegister)
        self._sio.on("joined", handler=self._onJoinGame)
        self._sio.on("created", handler=self._onCreatedGame)
        self._sio.on("state", handler=self._onState)

    # TODO: callbacks + coroutines = bad
    def registerCallbacks(self, *,
                          onRegister: Callable[[str], None] = None,
                          onJoinGame: Callable[[str], None] = None,
                          onCreatedGame: Callable[[str], None] = None):
        self._onRegisterCallback = onRegister
        self._onJoinGameCallback = onJoinGame
        self._onCreatedGameCallback = onCreatedGame

    @property
    def state(self) -> Dict:
        """ Returns state of agent. """
        return self.agent.state

    @property
    def playerId(self) -> str:
        """ Returns None if not registered. """
        return self._playerId

    @property
    def gameName(self) -> str:
        return self._gameName

    def connect(self, address: str):
        """ Connects Agent to the server. Server shoud respond emit 'handshake' after this.

        Warning: If name is invalid, this fails silently (server-side). """
        if self.playerId is not None:
            raise Exception("Agent already logged in")

        # playerId is autogenerated by the server, although it also relies on client caching
        # see dataacess-fake.js
        self._sio.connect(address)
        self._sio.emit("registerplayer", {"playerName": self.agent.name})

    def disconnect(self):
        if self._playerId is None:
            raise Exception("Agent already disconnected")

        self._playerId = None
        self._gameName = None
        self._sio.disconnect()

    def createGame(self):
        if self._playerId is None:
            raise Exception("An Agent needs to be logged in to play a game")

        self._sio.emit("create", {"playerName": self.agent.name})

    def joinGame(self, gameName: str):
        if self._playerId is None:
            raise Exception("An Agent needs to be logged in to play a game")
        if self._gameName is not None:
            raise Exception("Already playing a game")

        self._sio.emit("join", {
            "playerName": self.agent.name,
            "gameName": gameName,
            "password": ""
        })

    def _onRegister(self, data: Dict[str, object]):
        self._playerId = data["playerId"]
        if self._onRegisterCallback is not None:
            self._onRegisterCallback(self.playerId)

    def _onJoinGame(self, data: Dict[str, object]):
        self._gameName = data["gameName"]
        if self._onJoinGameCallback is not None:
            self._onJoinGameCallback(self.gameName)

    def _onCreatedGame(self, data: Dict[str, object]):
        # Creating a game does not mean you join it...
        self.joinGame(data["gameName"])
        if self._onCreatedGameCallback is not None:
            self._onCreatedGameCallback(data["gameName"])

    def _onState(self, data: Dict[str, object]):
        """Function to handle state updates"""
        # There's an odd case where the data is empty
        if data is None:
            print("Warning: Received empty state message")
            return

        state = GameState(data)
        # Automatically start a game
        if state.state == TreasonState.WAITING:
            if state.numPlayers >= self.agent.kplayer:
                self._sio.emit('command', {
                    'command': 'start',
                    'gameType': ' original',
                    'stateId': state.stateId
                })
        # we are in a game: use the agent to play
        else:
            vectorized_state = state_to_vector(state)
            # TO DO: make agent.process an actual function
            nn_output = self.agent.process(vectorized_state)
            emission_data = vector_to_emission(nn_output)
            # TO DO: verify if emission_data is a valid response given the state
            self._sio.emit('command', emission_data)
