import socketio

sio = socketio.Client()
sio.connect('http://localhost:8080')
#sio.emit('connect',{'foo':'bar'})

# sio.emit('registerplayer', {
#     "playerName": "benedict",
#     "playerId": 2
# })
# sio.emit('registerplayer', {
#     "playerName": "arnold",
#     "playerId": 3
# })
sio.emit('create',{
    'gameName': '1',
    'playerName': '',
    'password': ''
    })

sio.emit('join',{
   'gameName': '1',
   'playerName': 'benedict',
   'password': ''
   })
