import time

from agent import TreasonAgent
from agentWrapper import TreasonAgentWrapper

agent = TreasonAgent("benedict")
agent2 = TreasonAgent("arnold")

wrap = TreasonAgentWrapper(agent)
wrap2 = TreasonAgentWrapper(agent2)

global variable
variable = 0
print("variable is initialized to {}".format(variable))

def printRegister(thing):
    global variable
    print("onRegisterCallback: param is {}".format(thing))
    print("variable is {}".format(variable))
    variable = thing
    print("variable is now {}".format(variable))

def printJoin(thing):
    global variable
    print("onJoinCallback: param is {}".format(thing))
    print("variable is {}".format(variable))
    variable = thing
    print("variable is now {}".format(variable))

def createLobbyFn(players):
    def addOtherPlayers(gameName):
        for player in players:
            player.joinGame(gameName)
    return addOtherPlayers

lobby = createLobbyFn([wrap2])

wrap.registerCallbacks(
    onRegister=printRegister,
    onJoinGame=printJoin,
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

print("press enter to end the test")
input("")

wrap.disconnect()
wrap2.disconnect()
