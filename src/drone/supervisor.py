import logging
from pylsl import StreamInlet, resolve_stream

from src.drone.drone import Drone
from src.drone.instruction import *
from src.map.map import Map

from src.param.header import *

class Supervisor :

    def __init__(self, m: object = Map()) -> None:
        """Create an object """
        self.drone = Drone(URI, m)

        self.is_running = False
        self.inlet = None


    def start(self, serveur_name = "EEG_prediction") -> None:
        """Initialization of the stream LSL"""
        streams = resolve_stream('name', serveur_name)
        if streams:
            self.inlet = StreamInlet(streams[0])
            logging.debug("Stream inlet initialized.")

            """Start the drone"""
            self.drone.start()
            self.is_running = True
            logging.debug("Drone started and supervisor is running.")

        else:
            logging.error("No streams found.")
            raise RuntimeError("No streams found.")

    def stop(self) -> None :
        """Stop the drone"""
        self.drone.stop()
        self.is_running = False

        """It's not an obligation to stop the LSL stream"""

    def run(self) -> None:

        if self.inlet is None :
            logging.error("Inlet is not initialized. Cannot run supervisor")
            return

        try:
            while self.is_running :
                """Process the stream"""
                sample, timestamp = self.inlet.pull_sample()
                instruction = sample[0]

                if instruction=="0":
                    self.drone.move_drone(Right, velocity=VELOCITY)
                    
                elif instruction=="1":
                    self.drone.move_drone(Left, velocity=VELOCITY)

                elif instruction=="2":
                    self.drone.move_drone(Land, velocity=VELOCITY)
                    return

                elif instruction=="3":
                    self.drone.move_drone(Forward, velocity=VELOCITY)

                elif instruction=="4":
                    self.drone.move_drone(Back, velocity=VELOCITY)

                elif instruction=="5":
                    self.drone.move_drone(Up, velocity=VELOCITY)

                elif instruction=="6":
                   self.drone.move_drone(Down, velocity=VELOCITY) 
                  
        except KeyboardInterrupt:
            self.drone.stop()

        """If it's not enter in the while"""
        logging.debug("Supervisor is not running")





    
