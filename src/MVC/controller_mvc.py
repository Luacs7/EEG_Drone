from src.MVC.model_mvc import DroneModel
from src.MVC.view_mvc import DroneView

from src.param.header import *

class DroneController:
    def __init__(self) -> None:
        
        self.model = DroneModel(self)
        self.view = DroneView(self)
        
    def lsl_connection(self, name):
        if self.model.inlet is None:
            if self.model.lsl_server_connection(serveur_name=name):
                return True
            else:
                return False
        else:
            self.model.lsl_server_disconnection()
            return False


    def drone_start(self):
        self.model.speed=self.view.speed_slider.get()
        self.model.dist=self.view.DistanceBetwennPoint_slider.get()

        self.model.thread.start()
    
    def drone_stop(self):
        self.model.stop_drone()

    def run(self):
        self.view.mainloop()

    def map_size_update(self, x_size, y_size, z_size):
        self.model.drone.map.set_map_max_coordinates(x_size, y_size, z_size)
    
    def map_start(self):
        self.model.drone.map.set_drone_coordinates(x=self.view.start_coordinates[X],y=self.view.start_coordinates[Y],z=self.view.start_coordinates[Z])
    
    def map_update(self):
        self.view.open_toplevel_map()

if __name__ == "__main__":
    controller = DroneController()
    controller.run()