from benedict.agent import TreasonAgent
from benedict.gameEnum import TreasonState, TreasonRole, TreasonAction, TreasonCommand
from benedict.gameState import GameState
from benedict.nnio import vector_to_emission, cards, states, actions, commands 


# listification
def listify(spec, enum):
    return [1 if spec == e else 0 for e in enum]

class DummyAgent(TreasonAgent):

    def process(self, state: GameState):

        # build up the "nueral network" output as a list
        nn_output = [1] # assume we are going to take an command
        # otherwise we will just return [0] to NO-OP

        command = None # thing to do
        action = None # income or coup
        target = None # player to target
        reveal = None # card to reveal

        if state.state == TreasonState.WAITING:
            print("AAAAAAAAAAAAAAAAAAAAAAAAAH")
            return [0]

        if state.state == TreasonState.START_TURN:
            # only do something if it is our turn
            if state.playerTurn == state.selfId:
                # if we have 7 or more coins, coup someone
                if state.cash(state.selfId) >= 7:
                    action = TreasonAction.COUP
                    for i in range(1, state.numPlayers):
                        p = (i+state.selfId) % state.numPlayers
                        # if they have less than 2 cards face up
                        if sum([int(c[1]) for c in state.influence(p)]) < 2:
                            target = p
                            break
                # income
                else:
                    action = TreasonAction.INCOME
            else:
                return [0]

        if state.state == TreasonState.WAIT_CHALLENGE_RESPONSE:
            command = TreasonCommand.ALLOW

        if state.state == TreasonState.WAIT_BLOCK_RESPONSE:
            command = TreasonCommand.ALLOW

        if state.state == TreasonState.BLOCK_RESPONSE:
            command = TreasonCommand.ALLOW

        if state.state == TreasonState.REVEAL:
            # check if we are the one that needs to reveal
            if state.revealTarget == state.selfId:
                # pick an influence to reveal
                our_cards = state.influence(state.selfId)
                # check if we can reveal our first card
                if not our_cards[0][1]:
                    reveal = our_cards[0][0]
                else:
                    reveal = our_cards[1][0]

        if state.state == TreasonState.EXCHANGE:
            return [0]

        nn_output += listify(command, commands)
        nn_output += listify(action, actions)
        nn_output += listify(target, [i+1 for i in range(state.numPlayers-1)])
        nn_output += [0] # we will never block, so blockingRole bit is 0
        nn_output += listify(reveal, cards)
        nn_output += listify(None, cards) # exchange cards will always be 0
        nn_output += listify(None, cards)

        return vector_to_emission(nn_output)
