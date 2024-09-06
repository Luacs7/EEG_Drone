import threading
import time
from src.drone.drone import Drone
from src.drone.abstract_drone import AbstractDrone
from src.map.map import Map
from src.param.header import *
from src.param.exceptions import *
from cflib.utils import uri_helper
from abc import ABC, abstractmethod

class AbstractController() :
    
    @abstractmethod
    def __init__(
        self,
        drone: object = Drone(),
        map_: object = Map() 
        ) -> None:
        """ Instantiation of Controller class """
        self.logger = get_logger(self.__class__.__name__)
        
    
    @abstractmethod
    def open(self, uri = URI_RADIO) -> None: 
        """ Open connection with the drone """
        
    @abstractmethod
    def start(self) -> None:
        """ Open thread, and allows drone control """
        
    @abstractmethod
    def stop(self) -> None:
        """ Stop the drone """

    
        
        
    
        
    