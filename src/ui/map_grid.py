
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QGridLayout, QPixmap
from PySide2.QtGui import QIcon



class MapGrid(QWidget):
    
    def __init__(self, rows, cols, parent=None):
        super(MapGrid, self).__init__(parent)
        self.rows = rows
        self.cols = cols
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        # Initialize the grid with empty labels
        self.labels = {}
        for row in range(rows):
            for col in range(cols):
                label = QLabel()
                self.grid_layout.addWidget(label, row, col)
                self.labels[(row, col)] = label
                
                
    def update_icon(self, row, col, icon_path):
        if (row, col) in self.labels:
            pixmap = QPixmap(icon_path)
            self.labels[(row, col)].setPixmap(pixmap)

