import socketio

from typing import Callable, Dict

from agent import TreasonAgent


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
        # Automatically start a game
        print('GameId:', data['gameId'])
        print('Players:', len(data['players']))
        if data['state']['name'] == 'waiting-for-players' and len(data['players']) == self.agent.kplayer:
                self._sio.emit('command',{
                    'command': 'start',
                    'gameType':'original',
                    'stateId':str(data['stateId'])
                })
