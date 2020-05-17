'''
this file contains functions for
converting socketio state messages into the neural network input and
converting the neural network output into command messages
'''

# rotates a list so that the element at index i becomes index 0
def rotate(lst, i):
    return lst[i:]+lst[:i]

# general function for converting a string to a multiplexor list
def string_to_arr(s, possibilities):
    return [1 if p==s else 0 for p in possibilities]

cards = ["duke", "captain", "assassin", "contessa", "ambassador"]
states = ["start-of-turn", "action-response", "final-action-response", "block-response", "reveal-influence", "exchange"]
actions = ["coup", "income", "foreign-aid", "tax", "assassinate", "steal", "exchange"]
blocking_cards = ["duke", "captain", "contessa", "ambassador"]

# convert the dictionary into a vector (list)
# state is a dictionary as specified in the treason coup README
def state_to_vector(state):

    # rotate the players list so that the perspective is consistent
    my_id = state["playerIdx"]
    players = state["players"]
    players = rotate(players, my_id)

    # add information about each player's hand
    p_hands = []
    for p in players:
        for i in p["influence"]:
            p_hands += string_to_arr(i["role"], cards)
            p_hands += [int(i["revealed"])] # [1] if revealed else [0]
        p_hands += [p["cash"]]

    # open up the state data
    state = state["state"]

    # list representing whose turn it is
    p_turn = [int(i==state["playerIdx"]) for i in range(len(players))]

    # list representing possible game states
    g_state = string_to_arr(state["name"], states)

    # list representing current action
    action = string_to_arr(state["action"], actions)

    # list representing current target
    rotated_id = (state["target"]-my_id) % len(players)
    target = [1 if i==rotated_id else 0 for i in range(len(players))]

    # list representing blocking role
    block = string_to_arr(state["blockingRole"], blocking_cards)

    # list representing exchange options
    ops = state["exchangeOptions"]
    if len(ops) < 2: ops = ["", ""]
    exchange = []
    for i in ops:
       exchange += string_to_arr(i, cards) 

    # list representing which player needs to reveal 
    p_reveal = []
    if state["playerToReveal"]:
        rotated_id = (state["playerToReveal"] - my_id) % len(players)
        p_reveal = [1 if i == rotated_id else 0 for i in range(len(players))]
    else:
        p_reveal = [0 for p in players]


    # add the vectors together to get the total input vector
    return p_hands + p_turn + g_state + action + target + block + exchange + p_reveal

