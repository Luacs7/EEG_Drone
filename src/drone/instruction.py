class Direction :
    
    delta_x = 0
    delta_y = 0
    delta_z = 0
    
    def __str__(self) -> str:
        return ""


class Right(Direction):
    
    delta_x = +1
    delta_y = 0
    delta_z = 0
    
    def __str__(self) -> str:
        return "right"
    
    
class Left(Direction):
    
    delta_x = -1
    delta_y = 0
    delta_z = 0
    
    def __str__(self) -> str:
        return "left"
    
    
class Forward(Direction):
    
    delta_x = 0
    delta_y = +1
    delta_z = 0
    
    def __str__(self) -> str:
        return "forward"
    
    
class Back(Direction):
    
    delta_x = 0
    delta_y = -1
    delta_z = 0
    
    def __str__(self) -> str:
        return "back"
    
    
class Up(Direction):
    
    delta_x = 0
    delta_y = 0
    delta_z = +1
    
    def __str__(self) -> str:
        return "up"
    
    
class Down(Direction):
    
    delta_x = 0
    delta_y = 0
    delta_z = -1
    
    def __str__(self) -> str:
        return "down"

class Land(Direction):
    
    delta_x = 0
    delta_y = 0
    delta_z = 0
    
    def __str__(self) -> str:
        return "land"  
    
class Stop(Direction):

    def __str__(self) -> str:
        return "stop"  