import time

from benedict.agent import TreasonAgent
from benedict.agentWrapper import TreasonAgentWrapper

from benedict.gameState import GameState
from benedict.nnio import state_to_vector

K = 2 # the number of players in a game

#agent = TreasonAgent("benedict", K)
#agent2 = TreasonAgent("arnold", K)


#wrap = TreasonAgentWrapper(agent)
#wrap2 = TreasonAgentWrapper(agent2)

NAMES = "benedict1 arnold1 benedict2 arnold2 benedict3 arnold3 benedict4 arnold4".split()

agents = [TreasonAgentWrapper(TreasonAgent(name, K)) for name in NAMES]

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

#lobby = createLobbyFn([wrap2])
for a in agents:
    a.connect("http://localhost:8080")

lobby1 = createLobbyFn([agents[0],agents[1]])
agents[0].registerCallbacks(onCreatedGame=lobby1)
lobby2 = createLobbyFn([agents[2],agents[3]])
agents[2].registerCallbacks(onCreatedGame=lobby2)
lobby3 = createLobbyFn([agents[4],agents[5]])
agents[4].registerCallbacks(onCreatedGame=lobby3)
lobby4 = createLobbyFn([agents[6],agents[7]])
agents[6].registerCallbacks(onCreatedGame=lobby4)


# wrap.registerCallbacks(
#     onRegister=printRegister,
#     onJoinGame=printJoin,
#     onCreatedGame=lobby
# )

#wrap.connect("http://localhost:8080")
#wrap2.connect("http://localhost:8080")

time.sleep(0.01)
for i in range(len(agents)):
    if i % 2 == 0:
        agents[i].createGame()
#wrap.createGame()


# Co-routine doesn't modify variable
#print("Final: {}".format(variable))
#print(wrap2.gameName)

# Test nnio
start = time.time()
for i in range(5000):
    state_dict = {
        "stateId": 2,
        "gameId": 1,
        "playerIdx": 1,
        "players": [
            {  # Test empty influence list (waiting for players)
                "influence": [
                    #     {
                    #         "role": "unknown",
                    #         "revealed": False
                    #     },
                    #     {
                    #         "role": "assassin",
                    #         "revealed": True
                    #     }
                ],
                "cash": 7
            },
            {
                "influence": [
                    {
                        "role": "duke",
                        "revealed": False
                    },
                    {
                        "role": "ambassador",
                        "revealed": True
                    }
                ],
                "cash": 8
            }
        ],
        "state": {  # ignore the validity of this gamestate
            "playerIdx": 0,
            "name": "final-action-response",
            "target": 1,
            "action": "exchange",
            "exchangeOptions": ["ambassador", "duke"],
            "playerToReveal": 1,
            "blockingRole": "ambassador"
        }
    }
    game_state = GameState(state_dict)
    vectorization = state_to_vector(game_state)
    print(vectorization)
end = time.time()
print("Time for 5000 conversions to vector:", end - start)
print("Average time per call:",str((end - start) / 5.0)+"ms")


print("press enter to end the test")
input("")
for a in agents:
    a.disconnect()
#wrap.disconnect()
#wrap2.disconnect()
