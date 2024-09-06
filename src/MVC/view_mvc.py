import customtkinter as ctk
from CTkTable import*

from src.param.header import *

class DroneView(ctk.CTk):  #class DroneView heritage of class CTK
    
    def __init__(self, controller) -> None:
        super().__init__()

        self.controller=controller

        #Window
        self.title("Control panel for the drone")
        self.geometry("1080x920")

        self.toplevel_window=None

        #Start Button
        self.start_button = ctk.CTkButton(self, text="Start", fg_color="green", command=self.start)
        self.start_button.grid(row=9, column=0, pady=(10,10), padx=(10,10))
        self.stop_button = ctk.CTkButton(self, text="Stop", fg_color="red", command=self.stop)
        self.stop_button.grid(row=9, column=1, pady=(10,10), padx=(10,10))

        #Connect button
        self.connect_button = ctk.CTkButton(self, text="Connect", command=self.connection)
        self.connect_button.grid(row=0, column=1, pady=(10,10), padx=(10,10))
        self.entry_name_server = ctk.CTkEntry(self, placeholder_text="Server Name")
        self.entry_name_server.grid(row=0,column=0, pady=(10,10), padx=(10,10))

        #Speed slider
        self.speed_text = ctk.CTkLabel(self, text="Speed")
        self.speed_text.grid(row=4, column=1, pady=(10,10), padx=(10,10))
        self.speed_slider = ctk.CTkSlider(self, from_=0.1, to=2, number_of_steps=20, command=self.speed_slider_event)
        self.speed_slider.grid(row=5, column=1, pady=(10,10), padx=(10,10))

        #Distance betwenn point slider
        self.DistanceBetwennPoint_text = ctk.CTkLabel(self, text="Distance Betwenn Point")
        self.DistanceBetwennPoint_text.grid(row=4, column=0, pady=(10,10), padx=(10,10))
        self.DistanceBetwennPoint_slider = ctk.CTkSlider(self, from_=0.1, to=2, number_of_steps=20, command=self.distance_slider_event)
        self.DistanceBetwennPoint_slider.grid(row=5, column=0, pady=(10,10), padx=(10,10))

        # X Y Z slider for the definition of the map
        self.x_label=ctk.CTkLabel(self, text="Max x")
        self.y_label=ctk.CTkLabel(self, text="Max y")
        self.z_label=ctk.CTkLabel(self, text="Max z")
        
        self.x_label.grid(row=6, column=0, pady=(10,10), padx=(10,10))
        self.y_label.grid(row=6, column=1, pady=(10,10), padx=(10,10))
        self.z_label.grid(row=6, column=2, pady=(10,10), padx=(10,10))

        self.x_slider=ctk.CTkSlider(self, from_=0, to=20, number_of_steps=20, command=self.map_slider_event)
        self.y_slider=ctk.CTkSlider(self, from_=0, to=20, number_of_steps=20, command=self.map_slider_event)
        self.z_slider=ctk.CTkSlider(self, from_=0, to=20, number_of_steps=20, command=self.map_slider_event)

        self.x_slider.grid(row=7, column=0, pady=(10,10), padx=(10,10))
        self.y_slider.grid(row=7, column=1, pady=(10,10), padx=(10,10))
        self.z_slider.grid(row=7, column=2, pady=(10,10), padx=(10,10))

        #Start coordinates
        self.start_coordinates=[0,0,0]
        self.init_button = ctk.CTkButton(self, text="Initialization", command=self.init_event)
        self.init_button.grid(row=1, column=1, pady=(10,10), padx=(10,10))
        self.entry_init = ctk.CTkEntry(self, placeholder_text="Drone position [x,y,z]")
        self.entry_init.grid(row=1,column=0, pady=(10,10), padx=(10,10))


    def connection(self) -> None:
        self.connect_button.configure(state="disabled")  #Desactivate the button during the connection to the server
        
        if self.controller.lsl_connection(self.entry_name_server.get()):
            self.connect_button.configure(text="Disconnect", fg_color="red")
        else:
            self.connect_button.configure(text="Connect", fg_color="blue")
        
        self.connect_button.configure(state="normal")

    def start(self) -> None:
        self.open_toplevel_map()  
        self.controller.drone_start()
    
    def stop(self) -> None:
        self.controller.drone_stop()

    def map_slider_event(self, value_slider) -> None:
        x=self.x_slider.get()
        y=self.y_slider.get()
        z=self.z_slider.get()
        #value_slider not use because we take the value of the three slider in the same time

        self.controller.map_size_update(x,y,z)

        self.x_label.configure(text=f"Max x = {x}")
        self.y_label.configure(text=f"Max y = {y}")
        self.z_label.configure(text=f"Max z = {z}")

    def speed_slider_event(self, value) -> None:
        self.speed_text.configure(text=f"Speed = {value} m/s")
    
    def distance_slider_event(self, value) -> None:
        self.DistanceBetwennPoint_text.configure(text=f"Distance Betwenn Point = {value} m")

    def init_event(self):
        entry_text = self.entry_init.get()
        self.start_coordinates=list(map(int, entry_text.strip('[]').split(',')))
        self.controller.map_start()

    def open_toplevel_map(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self.controller)  # create window if its None or destroyed
            self.toplevel_window.update_top_level()
        else:
            self.toplevel_window.focus()  # if window exists focus it
            self.toplevel_window.update_top_level()


        

#######################Top level window##############################

class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self, controller):
        super().__init__()
        
        self.controller=controller

        self.geometry("400x300")

        self.label = ctk.CTkLabel(self, text="ToplevelWindow")
        self.label.grid(row=0, column=0, pady=(10,10), padx=(10,10))

        self.max_coordinates=controller.model.drone.map.get_max_coordinates()
        self.coordinates=self.controller.model.drone.map.get_drone_coordinates()
        self.old_coordinates=self.controller.view.start_coordinates

        #Table show the coordinates X and Y
        self.table=CTkTable(self, row=int(self.max_coordinates[Y]), column=int(self.max_coordinates[X]), width=self.max_coordinates[Y]*10, height=self.max_coordinates[X]*10)
        self.table.grid(row=1, column=0, pady=(10,10), padx=(10,10))

        #Altitude show the coordinate Z
        self.altitude=ctk.CTkProgressBar(self, orientation="vertical")
        self.altitude.set((1/self.max_coordinates[Z])*self.coordinates[Z])
        self.altitude.grid(row=1, column=1, pady=(10,10), padx=(10,10))


    def update_top_level(self):
        self.coordinates=self.controller.model.drone.map.get_drone_coordinates()
        self.table.insert(row=int(self.old_coordinates[Y]), column=int(self.old_coordinates[X]), value="O")
        self.table.insert(row=int(self.coordinates[Y]), column=int(self.coordinates[X]),value="X")
        self.old_coordinates=self.coordinates
