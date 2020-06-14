from enum import Enum


class TreasonState(Enum):
    WAITING = "waiting-for-players"
    START_TURN = "start-of-turn"  # Player turn given by playerIdx
    WAIT_CHALLENGE_RESPONSE = "action-response"  # Waiting for challenge
    WAIT_BLOCK_RESPONSE = "final-action-response"
    BLOCK_RESPONSE = "block-response"  # Waiting for challenge to target's response
    REVEAL = "reveal-influence"  # See playerToReveal
    EXCHANGE = "exchange"  # playerIdx chooses card to pick


class TreasonRole(Enum):
    """ 'not dealt' is not included. Should be treated as 'unknown'. """
    UNKNOWN = "unknown"
    DUKE = "duke"
    CAPTAIN = "captain"
    ASSASSIN = "assassin"
    CONTESSA = "contessa"
    AMBASSADOR = "ambassador"


class TreasonCommand(Enum):
    READY = "ready"
    START = "start"
    ADD_AI = "add-ai"
    ACTION = "play-action"
    BLOCK = "block"
    CHALLENGE = "challenge"
    ALLOW = "allow"
    REVEAL = "reveal"
    EXCHANGE = "exchange"
    INTERROGATE = "interrogate"  # unused
    LEAVE = "leave"


class TreasonAction(Enum):
    TAX = "tax"
    STEAL = "steal"
    ASSASSINATE = "assasinate"
    INTERROGATE = "interrogate"  # unused
    EXCHANGE = "exchange"
    INCOME = "income"
    F_AID = "foreign-aid"
    COUP = "coup"
