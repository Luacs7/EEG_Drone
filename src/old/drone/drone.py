
import time
import threading


from src.drone.control_values import ControlValues
from src.drone.abstract_drone import AbstractDrone
from src.param.header import *

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.positioning.motion_commander import MotionCommander

# Adresse URI du drone Crazyflie

class Drone(AbstractDrone) :
    
    def __init__(
        self,
        timeout_value: int = 1000,
        grided: bool = True
        ) -> None:
        
        cflib.crtp.init_drivers(enable_debug_driver=False)
        self.logger = get_logger(self.__class__.__name__)

        
        """ ATTRIBUTES """
        self._cf = Crazyflie(rw_cache='./cache')
        self.is_connected: bool = False
        self.is_running:bool    = False
        
        self.timeout_value = timeout_value
        self.grided = grided
        
        self.motor_power:int  = 0
        self.pitch: float     = 0
        self.row: float       = 0
        self.yaw: float       = 0

        """ INIT """
        self._set_callback()
        self.logger.debug(f"Drone instance created")
        
        
    """  HIGH LEVEL FUNCTIONS """
        
        
        
        
        
        
    """ LOW LEVEL FUNCTIONS """
    
    ''' Connection functions '''
    
    def open(self, uri = URI_RADIO) -> None:
        self.URI = uri 
        self._cf.open_link(uri)
        
    def close(self):
        self._cf.close_link()
        
    ''' High level motors functions '''
           
    def move(
        self,
        direction: str = NULL,
        distance: float = DISTANCE
        ) -> None:
        
        self.direction = direction
        self.distance = distance
        
    def start_procedure(self, frequency: float = 0.01) -> None:
        """ Open a thread to start procedure """
        if self.is_running:
            self.frequency = frequency
            self.is_running = True
            self.thread = threading.Thread(target=self._run_procedure)
            self.thread.start()
            print("Start procedure")
        else:
            print("Procedure is already running")
    
    def _run_procedure(self) -> None:
        
        """ Run normal using of drone in an other thread """
        with MotionCommander(self._cf) as mc:
            while self.is_running:
                
                time.sleep(self.frequency)
                
                # Set the movement direction based on input
                if self.direction == NULL:
                    pass
                
                elif self.direction == RIGHT:
                    mc.right(self.distance)
                    self.direction = NULL
                    
                elif self.direction == LEFT:
                    mc.left(self.distance)
                    self.direction = NULL

                elif self.direction == FORWARD:
                    mc.forward(self.distance)
                    self.direction = NULL
                    
                elif self.direction == BACK:
                    mc.back(self.distance)
                    self.direction = NULL
                    
                # elif self.direction == UP:
                #     mc.up(self.distance)
                #     self.direction = NULL
                    
                # elif self.direction == DOWN:
                #     mc.down(self.distance)
                #     self.direction = NULL
                    
                else: # Error
                    print("Wrong movement.")
                    self.is_running = False
    
    ''' Low level motors functions '''
    
    def init_motors(self):
        self.logger.debug(f"Intialization of motors")
        
        timeout = False
        timeout_counter = 0
        
        while not self.is_connected or timeout == False:
            
            time.sleep(0.1)
            timeout_counter += 100
            if timeout_counter >= self.timeout_value :
                timeout = True
            
        if self.is_connected : # Init drone motors
            self.logger.debug(f"Motors initialized")
            self.set_motors_value(0)
            time.sleep(0.2)
            self.set_motors_value(5000, mapped_value=False)
            
        else: # Timeout
            time.sleep(0.1)
            self.logger.warning(f"TIMEOUT")
            raise Exception("Timeout. Retry to open connexion with open().")
 
    def stop_motors(self):
        """ Stop all motors """
        self.set_motors_value(0)
        self.logger.debug(f"Motors stopped")
        
    def set_motors_value(
        self,
        thrust: int,
        roll: float = 0,
        pitch: float = 0,
        yaw: float = 0,
        mapped_value: bool = True 
        ) -> None:
        
        """ 
        Set the thrust value and rotation value,
        (between 0 and 65535)
        """
        
        if mapped_value :
            if thrust < 0 or thrust > 1:
                raise ValueError("Value must be between 0 and 1.")
            max_power = 65535
            self.motor_power = int(thrust * max_power)
            
        else : 
            self.motor_power = thrust 
        
        self._cf.commander.send_setpoint(0,0,0,0)
        self._cf.commander.send_setpoint(roll, pitch, yaw, self.motor_power)
        
    ''' Map functions '''
    
    ...
    
    
    """ PRIVATE FUNCTIONS """
    
    def _set_callback(self) -> None:
        """ Set all callbacks """
        self._cf.connected.add_callback(self._connected)
        self._cf.disconnected.add_callback(self._disconnected)
        self._cf.connection_failed.add_callback(self._connection_failed)
        self._cf.connection_lost.add_callback(self._connection_lost)
        
    def _connection_failed(self, link_uri, msg) -> None:
        """ Callback when connection initial connection fails (i.e no Crazyflie at the specified address) """
        print(f'Connection to {link_uri} failed: {msg}')
        self.is_connected = False

    def _connection_lost(self, link_uri, msg) -> None:
        """ Callback when disconnected after a connection has been made (i.e Crazyflie moves out of range) """
        print(f'Connection to {link_uri} lost: {msg}')
        self.is_connected = False

    def _disconnected(self, link_uri) -> None:
        """ Callback when the Crazyflie is fully disconnected (called in all cases) """
        print(f'Disconnected from {link_uri}')
        self.is_connected = False
    
    def _connected(self, link_uri) -> None:
        """ This callback is called when the Crazyflie has been connected and the TOCs have been downloaded. """
        print(f'Connected to {link_uri}')
        self.is_connected = True