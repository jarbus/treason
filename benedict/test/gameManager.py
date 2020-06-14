
from benedict.agent import TreasonAgent
from benedict.gameManager import TreasonGameManager
from benedict.dummyAgent import DummyAgent


# manager = TreasonGameManager(agent_count=40,
#                              room_size=4,
#                              game_addr="http://localhost:8080")
# print("Agents intialized.")

# manager.runGames()

class DummyGameManager(TreasonGameManager):

    def _createAgent(self, *, name: str, room_size: int) -> TreasonAgent:
        return DummyAgent(name=name, k=room_size)


manager = DummyGameManager(agent_count=50,
                           room_size=5,
                           game_addr="http://localhost:8080")
print("Agents intialized.")

manager.runGames()
