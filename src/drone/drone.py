import threading
from queue import Queue
import time
from src.map.map import Map
from src.param.header import *
from src.param.exceptions import *
from src.map.map_exception import *
from src.drone.instruction import *

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander

#URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

class Drone():

    def __init__(
        self,
        uri = URI,
        map_: object = Map() 
        ) -> None:
        
        cflib.crtp.init_drivers()
        self.logger = get_logger(self.__class__.__name__)
        
        ''' Attributes '''
        super().__init__()
        self.map = map_
        self.is_running = False
        self.distance: float = DISTANCE
        self.velocity: float = VELOCITY
        self.thread = threading.Thread(target=self._run)
        self.queue = Queue(16)
        self.logger.debug(f"{self.__class__.__name__} instance created ")
        self.uri = uri

        
    def start(self) -> None:
        """ Open thread, and allows drone control """
        
        self.logger.debug(f"Connexion etablished; URI = {self.uri}")
        self.is_running = True
        self.thread.start()
        

    def stop(self) -> None:
        """ Stop the drone"""
        
        self.logger.debug(f"Drone stop")
        self.queue.put(STOP)
        
        
    def emergency_stop(self) -> None:
        """ Stop the drone"""
        
        self.logger.debug(f"Drone stop")
        self.is_running = False
        self.queue.put(STOP)
        
        
    def move_drone(
        self, 
        instruction: Direction, 
        distance: float = DISTANCE, 
        velocity: float = VELOCITY
        ) -> None:
        """ 
        Move the drone from an instruction :
        Instructions can be found in instruction.py file
        """   
        
        if not self.is_running : raise NotInRunningException("Drone not in running")
        
        self.distance = distance
        self.velocity = velocity
        self.logger.debug(f"Instruction {str(instruction)} sent to the drone")
        self.queue.put(instruction)
        
        
    def _run(self):
        """ Run the drone in normal using """    
        
        self.logger.debug(f"Thread open, drone is running")
        
        with SyncCrazyflie(self.uri, cf=Crazyflie(rw_cache='./cache')) as scf:
            with MotionCommander(scf) as mc:
                while self.is_running:
                    # Get instruction from queue and process information
                    self._process_instruction(
                        self.queue.get(), 
                        mc, 
                        self.distance, 
                        self.velocity
                        )
                
        self.logger.debug(f"drone turned off correctly")
        
                
    def _process_instruction(
        self,
        instruction : Direction, 
        mc, 
        distance,
        velocity
        ) -> None:
        """
        Process the instruction
        """
        
        if instruction == Right :
            
            if self.map.check_and_set_next_position(Right):
                self.logger.debug(f"Drone go right at {distance} m at {velocity} m/s2")
                mc.right(distance,velocity=velocity)
            else : self.drone_out_of_map()
            
        elif instruction == Left:
            
            if self.map.check_and_set_next_position(Left):
                self.logger.debug(f"Drone go left at {distance} m at {velocity} m/s2")
                mc.left(distance,velocity=velocity)
            else : self.drone_out_of_map()
            
        elif instruction == Forward:
            
            if self.map.check_and_set_next_position(Forward):
                self.logger.debug(f"Drone go forward at {distance} m at {velocity} m/s2")
                mc.forward(distance,velocity=velocity)
            else : self.drone_out_of_map()

        elif instruction == Back:
            
            if self.map.check_and_set_next_position(Back):
                self.logger.debug(f"Drone go back at {distance} m at {velocity} m/s2")
                mc.back(distance,velocity=velocity)
            else : self.drone_out_of_map()

        elif instruction == Up:
            
            if self.map.check_and_set_next_position(Up):
                self.logger.debug(f"Drone go up at {distance} m at {velocity} m/s2")
                mc.up(distance,velocity=velocity)
            else : self.drone_out_of_map()

        elif instruction == Down:
            
            if self.map.check_and_set_next_position(Down):
                self.logger.debug(f"Drone go down at {distance} m at {velocity} m/s2")
                mc.down(distance,velocity=velocity)
            else : self.drone_out_of_map()

        elif instruction == Land:
            
            if self.map.check_and_set_next_position(Land):
                self.logger.debug(f"Drone land at {distance} m at {velocity} m/s2")
                mc.land(distance,velocity=velocity)
            else : self.drone_out_of_map()
            
        elif instruction == Stop:
            
            self.logger.debug(f"Drone go stop at {distance} m at {velocity} m/s2")
            mc.stop(distance,velocity=velocity)
            
        else: 
            self.logger.warning(f"Unknow instruction, drone go land")
            mc.land()


    def drone_out_of_map(self): #TODO drone_out_of_map
        self.logger.warning(f"Drone out of range")
        pass 