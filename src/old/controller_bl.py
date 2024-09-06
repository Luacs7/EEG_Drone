import threading
import time
from src.old.drone.drone import Drone
from src.old.drone.abstract_drone import AbstractDrone
from src.map.map import Map
from src.param.header import *
from src.param.exceptions import *
from old.abstract_controller import AbstractController


class Controller(AbstractController):

    URI = 'usb://0'
    URI_RADIO = 'radio://0/90/250K'
    URI_2 = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')
    

    def __init__(
        self,
        drone: object = Drone(),
        map_: object = Map() 
        ) -> None:
        
        ''' Attributes '''
        super().__init__()
        self.drone = drone
        self.map = map_
        self.power: int = 0
        self.running = False
        self.thread = threading.Thread(target=self._run)
        self.logger.debug(f"{self.__class__.__name__} instance created ")
        
    def open(
        self, 
        uri = URI_2,
        ) -> None: 
        """ Open connection with the drone """
        
        self.URI = uri 
        self.drone.open(uri=self.URI)
        self.logger.debug(f"Connexion etablised; URI = {self.URI}")
        
    def start(self) -> None:
        """ Open thread, and allows drone control """
        
        self.logger.debug(f"Drone start")
        self.running = True
        self.drone.init_motors()
        self.thread.start()
        
    def stop(self) -> None:
        """ Stop the drone"""
        
        self.logger.debug(f"Drone stop")
        self.running = False
        self.drone.stop_motors()
        self.drone.close()
        

        
        
        
        
    """ OLD """

        
        
    """ High Level """
    
    def start_drone(self):
        self.drone.start_procedure()
        
    def move_drone(self,direction):
        """
        Direction can be :
            - RIGHT
            - LEFT
            - FORWARD
            - BACK
         """
         
        if direction not in MOVEMENT:
            raise NotMovementException("Not a valid movement")
        
        self.drone.move(direction)
    
    
    """ Low Level """

    def increase_power(self,value: int = 5000):
        """ Increase the power of the drone (between 0 and 65535) """
        self.power += value

    def decrease_power(self,value: int = 5000):
        """ Decrease the power of the drone (between 0 and 65535) """
        self.power -= value

    def set_power(self):
        """ Set the power of the drone """
        self.drone.set_motors_value(self.power, mapped_value=False)

    def start_thread(self):
        pass
        
        
    def _run(self, sample: float = 0.01):
        """ 
        Function threaded which set the power 
        of the drone periodically (t = sample)
        """
        
        while self.running:
            self.set_power()
            time.sleep(sample)  # 100 Hz

    def stop_thread(self):
        self.running = False
        if self.thread is not None:
            self.thread.join()
            
    def replace_drone(self, movement: int) : 
        """ Move the drone """
        
        # Set the movement direction based on input
        if movement == RIGHT:
            roll = MOVE_RATE  # Roll to the right
            x_move = 1
            y_move = 0
            
        elif movement == LEFT:
            roll = - MOVE_RATE  # Roll to the left
            x_move = -1
            y_move = 0
            
        elif movement == FORWARD:
            pitch = MOVE_RATE  # Pitch forward
            x_move = 0
            y_move = 1
            
        elif movement == BACK:
            pitch = - MOVE_RATE  # Pitch backward
            x_move = 0
            y_move = -1
        
        # Move the drone
        self.drone.set_motors_value(
            self.power, 
            roll=roll if movement in (LEFT, RIGHT) else 0,
            pitch=pitch if movement in (UP, DOWN) else 0, 
            yaw=0, 
            mapped_value=False
            )
        
        time.sleep(2) # TODO ajust in function of spacing
        
        # Stop the movement after moving the specified distance
        self.drone.set_motors_value(self.power, roll=0, pitch=0, yaw=0, mapped_value=False)
        self.map.set_drone_coordinates(x=x_move, y=y_move)
    
    def hover(
        self, 
        cf, 
        duration, 
        height=0.5
        ) -> None:
        
        """
        Take off the drone and maintain it in a hover state.
        
        Args:
        cf: Instance of Crazyflie.
        duration: Duration of the hover in seconds.
        height: Height of the hover in meters (default is 0.5 m).
        """
        try:
            # Take off and hover
            print("Takeoff and hover")
            cf.commander.send_position_setpoint(0, 0, height, 0)
            time.sleep(duration)

            # Return to the starting position for landing
            print("Landing")
            cf.commander.send_position_setpoint(0, 0, 0, 0)
            time.sleep(2)
            
        finally:
            # Disconnect the drone
            cf.close_link()         
            
    def get_drone(self):
        return self.drone
    
    def get_cf(self):
        return self.drone.cf
          
        
          
if __name__ == '__main__':
    pass