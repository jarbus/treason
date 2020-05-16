import time

from agent import TreasonAgent
from agentWrapper import TreasonAgentWrapper

agent = TreasonAgent("benedict")
agent2 = TreasonAgent("arnold")

wrap = TreasonAgentWrapper(agent)
wrap2 = TreasonAgentWrapper(agent2)

variable = 0
print(variable)

def change(thing):
    variable = thing
    print("Change: {}".format(variable))

def createLobbyFn(players):
    def addOtherPlayers(gameName):
        for player in players:
            player.joinGame(gameName)
    return addOtherPlayers

lobby = createLobbyFn([wrap2])

wrap.registerCallbacks(
    onRegister=change,
    onJoinGame=change,
    onCreatedGame=lobby
)

wrap.connect("http://localhost:8080")
wrap2.connect("http://localhost:8080")

time.sleep(1)
wrap.createGame()

time.sleep(1)

# Co-routine doesn't modify variable
print("Final: {}".format(variable))
print(wrap2.gameName)
