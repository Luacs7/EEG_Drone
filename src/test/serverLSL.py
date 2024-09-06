import time
import keyboard
from pylsl import StreamInfo, StreamOutlet

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.controller.instruction import *

info = StreamInfo('EEG_prediction', 'Markers', 1, 0, 'string')
outlet = StreamOutlet(info)

while True:
    if keyboard.is_pressed('right'):
        outlet.push_sample("0")
        time.sleep(1)

    elif keyboard.is_pressed('left'):
        outlet.push_sample("1")
        time.sleep(1)
        
    elif keyboard.is_pressed('l'): #instruction for land
        outlet.push_sample("2")
        time.sleep(1)





