from typing import Dict


class TreasonAgent:
    """ Don't put the model in here. """

    def __init__(self, name: str, k: int):
        self.name = name
        self.kplayer = k

    @property
    def state(self) -> Dict:
        """ Returns state of agent. """
        pass

    def process(self, GameState: state):
        """ Returns vector output of the model, given the game state. """
        pass

    def reset(self):
        pass
