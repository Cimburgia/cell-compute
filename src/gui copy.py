import sys
import PyQt6.QtWidgets as QW
import PyQt6.QtCore as QC
import cell
import grid
from PyQt6.QtWidgets import QSizePolicy
from layout_colorwidget import Color

colors = {
    "wire":"lightpink",
    "nor":"gold",
    "empty":"powderblue"
}

class Main_Window(QW.QMainWindow):
    def __init__(self, plate):
        super().__init__()
        self.plate = plate
        self.size = plate.size
        self.setMinimumSize(QC.QSize(700, 500))
        self.setWindowTitle("Cell Compute")

        # Set central widget
        central_widget = QW.QWidget()
        self.setCentralWidget(central_widget)

        # Set high level layout
        self.base_layout = QW.QHBoxLayout(central_widget)
        self.plate_layout = QW.QGridLayout()
        self.side_panel_layout = QW.QVBoxLayout()
        self.base_layout.addLayout(self.plate_layout, 4)
        self.base_layout.addLayout(self.side_panel_layout, 1)
        self.plate_layout.setSpacing(0) 

        # Initialize widgets
        self.init_plate()
        self.init_side_panel()

    ## Initialization Methods ##
    def init_plate(self):
        """
        Initializes an empty plate to place a pattern. Each cell is a button that
        will be blank until updated.
        """
        self.buttons = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                button = QW.QPushButton()
                button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                button.setStyleSheet("""
                        QPushButton {
                            background-color:powderblue;
                            border: none;
                            margin: 1px;
                        }
                        """)
                button.clicked.connect(lambda checked, x=i, y=j: self.on_cell_click(x, y))
                self.plate_layout.addWidget(button, i, j)
                row.append(button)
            self.buttons.append(row)
        
    def init_side_panel(self):
        # Add three buttons
        for i in range(3):
            button = QW.QPushButton(f"Button {i+1}")
            button.clicked.connect(lambda checked, btn=i+1: print(f"Button {btn} clicked"))
            self.side_panel_layout.addWidget(button)

        # Add dropdown menu
        self.cell_type_dropdown = QW.QComboBox()
        self.cell_type_dropdown.addItems(["empty", "wire", "nor"])
        # self.dropdown.currentIndexChanged.connect(self.on_dropdown_change)
        self.side_panel_layout.addWidget(self.cell_type_dropdown)

        # Add stretch to push widgets to the top
        self.side_panel_layout.addStretch(1)
    
    ## Button Click Actions ##
    def on_cell_click(self, x, y):
        selected_type = self.cell_type_dropdown.currentText()
        print(selected_type)
        new_cell = cell.Cell(x, y, selected_type)
        self.plate.add_cell(x, y, new_cell)
        button = self.buttons[x][y]
        button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {colors[selected_type]};
                    border: none;
                    margin: 1px;
                }}
            """)
        
    def on_update_click(self):
        print(self.plate.show_grid())

if __name__ == "__main__":
    plate = grid.Grid(10)
    app = QW.QApplication(sys.argv)
    window = Main_Window(plate)
    window.show()
    sys.exit(app.exec())
