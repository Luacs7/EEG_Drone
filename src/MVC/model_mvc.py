import logging
import threading

from pylsl import StreamInlet, resolve_streams
from src.drone.drone import Drone
from src.map.map import Map
from src.drone.instruction import *
from src.param.header import *



class DroneModel:
    def __init__(self, controller, m: object = Map()) -> None:
        """Create an object """
        self.drone = Drone(URI, m)
        
        self.controller=controller

        self.is_running = False
        self.inlet = None

        self.speed=VELOCITY
        self.dist=DISTANCE

        self.thread = threading.Thread(target=self.start_drone)

    #################### Link with a LSL sever ###############################
    def lsl_server_connection(self, serveur_name="EEG_prediction", timeout=2) -> bool:
        streams = resolve_streams(wait_time=timeout)
        filtered_streams = [stream for stream in streams if stream.name() == serveur_name]

        if filtered_streams:
            self.inlet = StreamInlet(filtered_streams[0])
            logging.debug("Stream inlet initialized.")
            return True
        else:
            logging.error(f"No streams found with name '{serveur_name}' within {timeout} seconds.")
            return False
        
        
    def lsl_server_disconnection(self):
        del self.inlet
        self.inlet=None
        logging.debug("Stream inlet reinitialized.")
    
    #################### Command the drone ###############################
    def start_drone(self):
        self.drone.start()
        self.is_running = True
        logging.debug("Drone started and supervisor is running.")

        while self.is_running : #Maybe interruption on the lsl server will be better
                """Process the stream"""
                sample, timestamp = self.inlet.pull_sample()
                instruction = sample[0]

                if instruction=="0":
                    self.drone.move_drone(Right, velocity=self.speed, distance=self.dist)
                    self.controller.map_update()
                    
                elif instruction=="1":
                    self.drone.move_drone(Left, velocity=self.speed, distance=self.dist)
                    self.controller.map_update()
                elif instruction=="2":
                    self.drone.move_drone(Land, velocity=self.speed, distance=self.dist)
                    self.controller.map_update()

                elif instruction=="3":
                    self.drone.move_drone(Forward, velocity=self.speed, distance=self.dist)
                    self.controller.map_update()

                elif instruction=="4":
                    self.drone.move_drone(Back, velocity=self.speed, distance=self.dist)
                    self.controller.map_update()

                elif instruction=="5":
                    self.drone.move_drone(Up, velocity=self.speed, distance=self.dist)
                    self.controller.map_update()
                elif instruction=="6":
                    self.drone.move_drone(Down, velocity=self.speed, distance=self.dist)
                    self.controller.map_update()
                   
    def stop_drone(self):
        if self.is_running:
            self.drone.stop()
            self.is_running=False
            self.thread.join()
            
            

