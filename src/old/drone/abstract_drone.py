

from src.old.drone.control_values import ControlValues

import time
from abc import ABC, abstractmethod

class AbstractDrone(ABC) :
    
    def __init__(self,timeout_value:int=1000) -> None:
        self.motor_power = 10001

        
    """ PUBLIC FUNCTIONS """
    
    ''' Connection functions '''
    
    @abstractmethod
    def open(self,uri='usb://0') -> None:
        pass
        
    @abstractmethod
    def close(self):
        pass

    ''' Motors functions '''
    
    @abstractmethod
    def init_motors(self):
        pass
        
    @abstractmethod
    def stop_motors(self):
        pass
        
    @abstractmethod
    def set_motors_value(self,thrust:int,roll:float=0,pitch:float=0,yaw:float=0,mapped_value=True):
        pass        
            
   