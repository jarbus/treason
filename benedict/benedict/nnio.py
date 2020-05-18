'''
this file contains functions for
converting socketio state messages into the neural network input and
converting the neural network output into command messages
'''
from benedict.gameEnum import TreasonState, TreasonRole, TreasonAction
from benedict.gameState import GameState

# rotates a list so that the element at index i becomes index 0
# def rotate(lst, i):
#     return lst[i:]+lst[:i]

# general function for converting a string to a multiplexor list
# def string_to_arr(s, possibilities):
#     return [1 if p==s else 0 for p in possibilities]

# cards = ["duke", "captain", "assassin", "contessa", "ambassador"]
# states = ["start-of-turn", "action-response", "final-action-response", "block-response", "reveal-influence", "exchange"]
# actions = ["coup", "income", "foreign-aid", "tax", "assassinate", "steal", "exchange"]
# blocking_cards = ["duke", "captain", "contessa", "ambassador"]

cards = {  # Enums are hashable
    TreasonRole.DUKE: 0,
    TreasonRole.CAPTAIN: 1,
    TreasonRole.ASSASSIN: 2,
    TreasonRole.CONTESSA: 3,
    TreasonRole.AMBASSADOR: 4
}

blocking_cards = {
    TreasonRole.DUKE: 0,
    TreasonRole.CAPTAIN: 1,
    TreasonRole.CONTESSA: 2,
    TreasonRole.AMBASSADOR: 3
}

states = {
    TreasonState.START_TURN: 0,
    TreasonState.WAIT_CHALLENGE_RESPONSE: 1,
    TreasonState.WAIT_BLOCK_RESPONSE: 2,
    TreasonState.BLOCK_RESPONSE: 3,
    TreasonState.REVEAL: 4,
    TreasonState.EXCHANGE: 5
}

actions = {
    TreasonAction.COUP: 0,
    TreasonAction.INCOME: 1,
    TreasonAction.F_AID: 2,
    TreasonAction.TAX: 3,
    TreasonAction.ASSASSINATE: 4,
    TreasonAction.STEAL: 5,
    TreasonAction.EXCHANGE: 6
}

commands = [
    TreasonCommand.ACTION,
    TreasonCommand.BLOCK,
    TreasonCommand.CHALLENGE,
    TreasonCommand.ALLOW,
    TreasonCommand.REVEAL,
    TreasonCommand.EXCHANGE
]

# convert the dictionary into a vector (list)
# state is a dictionary as specified in the treason coup README
def state_to_vector(state: GameState):
    card_vec_size = len(cards) + 1

    player_vec_size = (card_vec_size * 2) + 1
    players_vec_size = player_vec_size * state.numPlayers
    # (turn, target, reveal) + (exchange) + (state) + (action) + (blocking)
    game_vec_size = (3*state.numPlayers) + (2*len(cards)) + len(states) + len(actions) + len(blocking_cards)

    # https://stackoverflow.com/questions/20816600/best-and-or-fastest-way-to-create-lists-in-python
    vec = [0] * (players_vec_size + game_vec_size)

    # rotate the players list so that the perspective is consistent
    for counter in range(state.numPlayers):
        player_idx = (counter + state.selfId) % state.numPlayers
        influences = state.influence(player_idx)

        player_vec_start = player_idx * player_vec_size
        for card_idx, (card, revealed) in enumerate(influences):
            # Start of this specific influence's vector
            card_vec_start = player_vec_start + (card_idx * card_vec_size)
            if card in cards:  # TreasonRole.UNKNOWN
                vec[card_vec_start + cards[card]] = 1
            vec[card_vec_start + len(cards)] = int(revealed)
        vec[player_vec_start + (2 * card_vec_size)] = state.cash(player_idx)

    # list representing current turn
    start_position = players_vec_size
    if state.playerTurn is not None:
        vec[start_position + state.playerTurn] = 1

    # list representing current state
    start_position += state.numPlayers
    if state.state != TreasonState.WAITING:
        vec[start_position + states[state.state]] = 1

    # list representing current action
    start_position += len(states)
    if state.currentAction is not None:
        vec[start_position + actions[state.currentAction]] = 1

    # list representing current target
    start_position += len(actions)
    if state.playerTurn is not None and state.target is not None:
        rotated_id = (state.target - state.playerTurn) % state.numPlayers
        vec[start_position + rotated_id] = 1

    # list representing blocking role
    start_position += state.numPlayers
    if state.blockingRole is not None:
        vec[start_position + blocking_cards[state.blockingRole]] = 1

    # list representing exchange options
    start_position += len(blocking_cards)
    if state.exchanges is not None:
        for idx, card in enumerate(state.exchanges):
            exchange_card_start = start_position + (idx * len(cards))
            vec[exchange_card_start + cards[card]] = 1

    # list representing which player needs to reveal
    start_position += 2*len(cards)
    if state.revealTarget is not None:
        rotated_id = (state.revealTarget - state.selfId) % state.numPlayers
        vec[start_position + rotated_id] = 1

    return vec



# the output vector is subdivided into regions specifying the confidence with
# respect to certain actions, and this functions parses out the meaning
def vec_argmax(vector, offset, enum):
    res = ""
    confidence = -1.0
    for i,e in enumerate(enum):
        val = vector[offset+i] 
        if val > confidence:
            res = e
            confidence = val
    return res


# convert the neural network's output into a python dictionary which can be .emit-ed to the server as a command
def vector_to_state(vector, state: GameState):
    # a python dictionary representing the emission the bot sends to the server
    emission = dict()
    # vector offset
    start_position = 0

    # command
    command = vec_argmax(vector, start_position, commands)
    emission["command"] = command
    start_position += len(commands)

    # action
    if command == TreasonCommand.ACTION:
        action = vec_argmax(vector, start_position, enum)
        emission["action"] = action
    start_position += len(actions)

    # target
    if "action" in emission and emission["action"] in {TreasonAction.STEAL, TreasonAction.ASSASSINATE, TreasonAction.COUP}:
        target = vec_argmax(vector, offset, [i+1 for i in range(numPlayers-1)])
        target = (target-state.selfId) % len(state.players)
        emission["target"] = target
    start_position += len(actions)

    # blockingRole
    if commmand == TreasonCommand.BLOCK:
        blockingRole = ""
        cur = state.currentAction
        if cur == TreasonAction.F_AID:
            blockingRole = TreasonRole.DUKE
        if cur == TreasonAction.ASSASSINATE:
            blockingRole = TreasonRole.CONTESSA
        # if current action is steal, interpret this to be captain versus ambassador
        if cur == TreasonAction.STEAL:
           if vector[start_position] < 0.5
                blockingRole = TreasonRole.CAPTAIN
            else
                blockingRole = TreasonRole.AMBASSADOR
        emission["blockingRole"] = blockingRole
    start_position += 1

    # challenge and allow commands have no additional paramaters, so we move on

    # reveal ("role")
    if command == TreasonCommand.REVEAL:
        card = vec_argmax(vector, start_position, cards)
        emission["role"] = card
    start_position += len(cards)

    # exchange ("roles")
    if command == TreasonCommand.EXCHANGE:
        card1 = vec_argmax(vector, start_position, cards)
        start_position += len(cards)
        card2 = vec_argmax(vector, start_position, cards)
        emission["roles"] = [card1, card2]
        
    return emission


    




