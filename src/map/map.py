from src.map.map_exception import *
from src.param.header import *

from src.param.header import *


class Map : 
    
    """
    Map is definie between : 
        [0,max_x[
        [0,max_y[
        [0,max_z[
    """
    
    def __init__(
        self,
        max_x: int = 5, 
        max_y: int = 5, 
        max_z: int = 2,
        spacing_x: int = 1,
        spacing_y: int = 1,
        spacing_z: int = 1,
        drone_coordinates: list = [0, 0, 0]
        ) -> None:
        
        """
        Create an instance of Map.

        Args: 
            max_x (int): The maximum x-coordinate value for the map. Default is 5.
            max_y (int): The maximum y-coordinate value for the map. Default is 5.
            max_z (int): The maximum z-coordinate value for the map. Default is 2.
            spacing_x (int): The spacing between points on the x-axis. Default is 1 metter.
            spacing_y (int): The spacing between points on the y-axis. Default is 1 metter.
            spacing_z (int): The spacing between points on the y-axis. Default is 1 metter.
            drone_coordinates (list): A list containing the initial coordinates [x, y, z] of the drone. Default is [0, 0, 0].

        Returns:
            None

        Raises:
            CoordinatesError: If the input coordinates are not in the correct format.
        """
        
        self.logger = get_logger(self.__class__.__name__)
        self.logger.debug(f"{self.__class__.__name__} instance created ")
        
        
        ''' Attributes '''
        self.max_x = max_x
        self.max_y = max_y
        self.max_z = max_z
        self.spacing_x = spacing_x
        self.spacing_y = spacing_y
        self.spacing_z = spacing_z
        self.drone_coordinates = drone_coordinates
        
        ''' Error check '''
        if(
            drone_coordinates[X] >= self.max_x or
            drone_coordinates[Y] >= self.max_y or
            drone_coordinates[Z] >= self.max_z or
            drone_coordinates[X] < 0 or
            drone_coordinates[Y] < 0 or
            drone_coordinates[Z] < 0 
        ):
            raise CoordinatesError(f"Drone out of range, please set up drone coordinates between (0, 0, 0) and ({self.max_x}, {self.max_y}, {self.max_z})")
        
        if not len(drone_coordinates) == 3 :
            raise CoordinatesError(f"The drone_coordinates list must be size 3")
        
        
    def __str__(self) -> str:
        return f"Map grid : ({self.max_x}, {self.max_y}, {self.max_z}) with spacing of {self.spacing_x} m for x, {self.spacing_y} m for y and {self.spacing_z} m for z, drone at posoition ({self.drone_coordinates[X]}, {self.drone_coordinates[Y]}, {self.drone_coordinates[Z]})"
        
    
    def __repr__(self) -> str:
        return f"Map(max_x={self.max_x}, max_y={self.max_y}, max_z={self.max_z}, spacing_x={self.spacing_x}, spacing_y={self.spacing_y}, spacing_z={self.spacing_z}, drone_coordinates={self.drone_coordinates})"
        
        
    """ PUBLIC FUNCTIONS """
    
    def set_drone_coordinates(
        self, 
        x: int = 0, 
        y: int = 0, 
        z: int = 0
        ) -> None:
        
        ''' Error check '''
        if (
            x >= self.max_x or 
            y >= self.max_y or
            z >= self.max_z or
            x < 0 or 
            y < 0 or
            z < 0 
            ):
            
            self.logger.warning(f"CoordinatesError, coordinates is : {x}, {y}, {z}")
            raise CoordinatesError(f"Drone out of range, please set up drone coordinates between (0, 0, 0) and ({self.max_x}, {self.max_y}, {self.max_z})")

        #set the coordinates
        self.x = x
        self.y = y
        self.z = z

        self.logger.debug(f"Set drone coordinates at {x}, {y}, {z}.")

    def set_map_max_coordinates(
        self, 
        max_x: int = 0, 
        max_y: int = 0, 
        max_z: int = 0
        ) -> None:
        
        ''' Error check '''
        if (
            max_x < 0 or 
            max_y < 0 or
            max_z < 0 
            ):
            
            self.logger.warning(f"CoordinatesError, Max coordinates is : {max_x}, {max_y}, {max_z}")
            raise CoordinatesError(f"Max coordinates is not valid")

        #Set max coordinates
        self.max_x=max_x
        self.max_y=max_y
        self.max_z=max_z

        self.logger.debug(f"Set max coordinates at {max_x}, {max_y}, {max_z}.")
        

    def get_drone_coordinates(self) -> list:
        return self.drone_coordinates
    
    def get_max_coordinates(self) -> list:
        return [self.max_x, self.max_y, self.max_z]
         
    
    
    def check_and_set_next_position(self, instruction) -> bool:
        """ 
        Check the new position.
        Return False if next position is out of map, else True.
        """
        
        self.logger.debug(f"instruction is {str(instruction)}")
        
        if ( # Out of map
            self.drone_coordinates[X] + instruction.delta_x >= self.max_x or 
            self.drone_coordinates[Y] + instruction.delta_y >= self.max_y or
            self.drone_coordinates[Z] + instruction.delta_z >= self.max_z or
            self.drone_coordinates[X] + instruction.delta_x < 0 or 
            self.drone_coordinates[Y] + instruction.delta_y < 0 or
            self.drone_coordinates[Z] + instruction.delta_z < 0
        ) : 
            self.logger.debug(f"drone out of map")
            return False
        
        else : 
            self.drone_coordinates[X] += instruction.delta_x
            self.drone_coordinates[Y] += instruction.delta_y
            self.drone_coordinates[Z] += instruction.delta_z
            self.logger.debug(f"Map coordinate update")
            return True
        