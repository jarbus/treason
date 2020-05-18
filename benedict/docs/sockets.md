The following are all types of socket.on calls
==============================================

```
'connect' client.js:193
'handshake' client.js:200
'updategames' client.js:208
'updateplayers' client.js:211
'globalchatmessage' client.js:214
'alert' client.js:220
'disconnect' client.js:224
'state' client.js:230
'history' client.js:250
'chat' client.js:269
'created' client.js:282
'joined' client.js:287
'error' client.js:302
'game-error' client.js:305
'rankings' client.js:308
'gamenodefound' client.js:311
'incorrectpassword' client.js:316
```

Socket.emit() calls
===================
```
'registerplayer' client.js:195,344
'join' client.js:328
'create' client.js:359
'showmyrank' client.js:369
'showrankings' client.js:372
'chat' client.js:854
'sendglobalchatmessage' client.js:870
```


There is also a command function, which has other socket.emit() calls:
===========================================

```
'ready' client.js:322
'start' client.js:405
'add-ai' client.js:417
'play-action' client.js:514,523
'block' client.js:638,642
'challenge' client.js:647
'allow' client.js:652
'reveal' client.js:679
'exchange' client.js:715
'interrogate' client.js:721
'leave' client.js:730
```
