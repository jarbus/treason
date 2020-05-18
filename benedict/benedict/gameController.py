import time
import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument('num_games',help="number of games you want to manage", type=int)
parser.add_argument('game_size',help="number of players in each game", type=int)
args = parser.parse_args()

from benedict.agent import TreasonAgent
from benedict.agentWrapper import TreasonAgentWrapper

from benedict.gameState import GameState
from benedict.nnio import state_to_vector

NAME_FILE=open('../../names.txt','r')
names = [name.strip() for name in NAME_FILE]
print(names)


def createLobbyFn(players):
    def addOtherPlayers(gameName):
        for player in players:
            player.joinGame(gameName)
    return addOtherPlayers


for game in range(args.num_games):
    lobby_agents = [TreasonAgentWrapper(TreasonAgent(random.choice(names), args.game_size)) for i in args.game_size]
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


for i in range(len(agents)):
    if i % 2 == 0:
        agents[i].createGame()

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
    state_to_vector(game_state)
end = time.time()
print("Time for 5000 conversions to vector:", end - start)
print("Average time per call:",str((end - start) / 5.0)+"ms")


print("press enter to end the test")
input("")
for a in agents:
    a.disconnect()
