import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PySide2.QtGui import QIcon

from src.ui.map_grid import MapGrid
from src.drone.drone import Drone

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        # Configuration de la fenêtre principale
        self.setWindowTitle("Mon Application")
        self.setGeometry(300, 300, 300, 200)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QVBoxLayout()

        # Layout du header
        header_layout = QVBoxLayout()
        title_label = QLabel("Titre de l'application")
        header_layout.addWidget(title_label)

        # Layout des boutons
        button_layout = QVBoxLayout()
        up_button = QPushButton("Up")
        up_button.setIcon(QIcon("path_to_up_icon.png"))  # Remplacez par le chemin vers votre icône "up"
        up_button.clicked.connect(self.controller.increase_power)
        down_button = QPushButton("Down")
        down_button.setIcon(QIcon("path_to_down_icon.png"))  # Remplacez par le chemin vers votre icône "down"
        down_button.clicked.connect(self.controller.decrease_power)
        
        stop_button = QPushButton("STOP")
        stop_button.clicked.connect(self.controller.stop)
        
        button_layout.addWidget(up_button)
        button_layout.addWidget(down_button)
        button_layout.addWidget(stop_button)
        
        # Ajout des layouts au layout principal
        main_layout.addLayout(header_layout)
        main_layout.addLayout(button_layout)
        
        
        # Configuration du layout principal
        central_widget.setLayout(main_layout)
        
        
    def map_widgets(self):
        self.map_grid = MapGrid()
        
        
    def menu_widgets(self):
        pass
    
    
    def header_widgets(self):
        
    
    
    def