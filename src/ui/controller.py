
from src.ui.ui import MainWindow
from src.drone.drone import Drone

class Controller:
    
    def __init__(
        self, 
        drone:Drone = Drone(), 
        ui:MainWindow = MainWindow()
        ) -> None:
        
        self.drone: Drone = drone
        self.ui: MainWindow = ui
    
    
    def set_signals():
        pass