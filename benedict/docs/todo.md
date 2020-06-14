# Todo
* Game manager
* `vector_to_state`
* Training/gradient manager
* a3c model seems promising
* make library a module

# Race Condition
during training, priority for challenging determined by id, with randomizing ids between games this should be fine
during online play, add delay of 3s before challenging

# Model
PPO for training,
LSTM core or attention network for model
