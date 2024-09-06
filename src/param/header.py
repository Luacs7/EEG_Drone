from cflib.utils import uri_helper
from src.log.logging_config import get_logger

""" URI """
URI_USB = 'usb://0'
#radio
URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

""" Drone movement"""
NULL     = "null"
RIGHT    = "right"
LEFT     = "left"
UP       = "up"
DOWN     = "down"
FORWARD  = "forward"
BACK     = "back"
STOP     = "stop"

MOVEMENT = [
    NULL,
    RIGHT,
    LEFT,
    FORWARD,
    BACK, #TODO Add up and down
]

DISTANCE = 0.5
VELOCITY = 0.5


MOVE_RATE = 1.0

""" Map """
X = 0
Y = 1
Z = 2