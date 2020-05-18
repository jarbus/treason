'''
this file contains functions for
converting socketio state messages into the neural network input and
converting the neural network output into command messages
'''
from gameEnum import TreasonState, TreasonRole, TreasonAction
from gameState import GameState

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

# convert the dictionary into a vector (list)
# state is a dictionary as specified in the treason coup README
def state_to_vector(state: GameState):
    card_vec_size = len(cards) + 1

    player_vec_size = ((card_vec_size * 2) + 1) * state.numPlayers
    # (turn, target, reveal) + (exchange) + (state) + (action) + (blocking)
    game_vec_size = (3*state.numPlayers) + (2*len(cards)) + len(states) + len(actions) + len(blocking_cards)

    # https://stackoverflow.com/questions/20816600/best-and-or-fastest-way-to-create-lists-in-python
    vec = [0] * (player_vec_size + game_vec_size)

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
    start_position = player_vec_size
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
