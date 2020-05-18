from typing import Dict, List, Tuple
from benedict.gameEnum import TreasonState, TreasonRole, TreasonAction


class Player:

    def __init__(self, roles: List[Tuple[TreasonRole, bool]], cash: int):
        self.roles = roles
        self.cash = cash


class GameState:

    def __init__(self, data: Dict[str, object]):
        self._stateId = data["stateId"]
        self._gameId = data["gameId"]
        self._selfId = data["playerIdx"]
        self._players = []
        for player in data["players"]:
            if player["influence"]:  # if empty list
                roles = [(TreasonRole(i["role"]), i["revealed"]) for i in player["influence"]]
                self._players.append(Player(roles, player["cash"]))
            else:
                roles = [(TreasonRole.UNKNOWN, False), (TreasonRole.UNKNOWN, False)]
                self._players.append(Player(roles, player["cash"]))

        # Everything but name might not be initialized
        state = data["state"]
        self._state = TreasonState(state["name"])
        self._player = state["playerIdx"] if "playerIdx" in state else None
        self._target = state["target"] if "target" in state else None
        self._exchanges = [TreasonRole(r) for r in state["exchangeOptions"]] if "exchangeOptions" in state else None
        self._blockingRole = TreasonRole(state["blockingRole"]) if "blockingRole" in state else None
        self._reveal = state["playerToReveal"] if "playerToReveal" in state else None
        self._action = TreasonAction(state["action"]) if "action" in state else None

    @property
    def gameId(self) -> int:
        return self._gameId

    @property
    def stateId(self) -> int:
        return self._stateId

    @property
    def selfId(self) -> int:
        return self._selfId

    @property
    def state(self) -> TreasonState:
        return self._state

    @property
    def playerTurn(self) -> int:
        return self._player

    @property
    def numPlayers(self) -> int:
        return len(self._players)

    def influence(self, player: int) -> List[Tuple[TreasonRole, bool]]:
        return self._players[player].roles

    def cash(self, player: int) -> int:
        return self._players[player].cash

    @property
    def exchanges(self) -> List[TreasonRole]:
        return self._exchanges

    @property
    def target(self) -> int:
        """ None if not applicable """
        return self._target

    @property
    def blockingRole(self) -> TreasonRole:
        return self._blockingRole

    @property
    def revealTarget(self) -> int:
        """ None if not applicable """
        return self._reveal

    @property
    def currentAction(self) -> TreasonAction:
        return self._action
