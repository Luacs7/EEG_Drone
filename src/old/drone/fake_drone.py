from src.drone.control_values import ControlValues
from src.drone.abstract_drone import AbstractDrone


import time

class FakeDrone(AbstractDrone) :
    
    def __init__(self,timeout_value:int=1000) -> None:
        self.motor_power = 10001

        
    """ PUBLIC FUNCTIONS """
    
    ''' Connection functions '''
    
    def open(self,uri='usb://0') -> None:
        print("FAKE - Drone connection open")
        
        
    def close(self):
        print("FAKE - Drone connection close")


    
    ''' Motors functions '''
    
    def init_motors(self):
        print("FAKE - Drone motors initialized")
        
        
    
    def stop_motors(self):
        print("FAKE - Drone motors stopped")

        
        
    def set_motors_value(self,thrust:int,roll:float=0,pitch:float=0,yaw:float=0,mapped_value=True):
        """ Set the thrust value and rotation value """
        
        if mapped_value :
            if thrust < 0 or thrust > 1:
                raise ValueError("Value must be between 0 and 1.")
            max_power = 65535
            self.motor_power = int(thrust * max_power)
            
        else : 
            self.motor_power = thrust 
        
        print(f"FAKE - Drone power of motors setup at {self.motor_power}.")
        
        
    def test_motors(self,t=1.5):
        """ Active propellers sloly during few seconds """
        print("Motor test")
        self.set_motors_value(10001)
        time.sleep(t)
        self.stop_motors()
            
   