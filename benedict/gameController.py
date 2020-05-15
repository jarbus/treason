import socketio
import time

sio = socketio.Client()

my_state = None

@sio.event
def state(data):
    print(data)
    global my_state
    my_state = data
    print(my_state['stateId'])

sio.connect('http://localhost:8080')
sio2 = socketio.Client()
sio2.connect('http://localhost:8080')

sio.emit('registerplayer', {
    "playerName": "benedict",
    "playerId": 2
})
sio2.emit('registerplayer', {
    "playerName": "arnold",
    "playerId": 3
})
sio.emit('create',{
    'gameName': '1',
    'playerName': 'benedict',
    'password': ''
    })

sio.emit('join',{
   'gameName': '1',
   'playerName': 'benedict',
   'password': ''
   })
sio2.emit('join',{
  'gameName': '1',
  'playerName': 'arnold',
  'password': ''
  })

#time.sleep(1)
#sio2.emit('command',{
#    'command':'ready',
#    'stateId':str(my_state['stateId'])
#    })

time.sleep(1)
sio.emit('command',{
    'command': 'start',
    #'action':'',
    #'target':'',
    #'blockingRole': '',
    #'role':'',
    #'roles':[''],
    'gameType':'original',
    'stateId':str(my_state['stateId'])
    })
