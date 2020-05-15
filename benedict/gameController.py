import socketio
# data = {
#     'command': "challenge",        # The name of the command: play-action, block, challenge, allow, reveal, exchange
#     'action': "",         # For the play-action command, the action to play
#     'target': 0,          # When playing an action which targets another player, the index of the player to target
#     'blockingRole': "",   # For the block command, the role to block with
#     'role': "",           # For the reveal command, the role to reveal
#     'roles': [""],        # For the exchange command, the role(s) you wish to keep
#     'stateId': 1          # Must match the stateId from the latest game state
# }

target_host = "localhost"

target_port = 8080  # create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
client.connect((target_host,target_port))
