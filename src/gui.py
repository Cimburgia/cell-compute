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
    "empty":"powderblue",
    "C6":"mediumvioletred",
    "C12":"darkcyan"
}

class Main_Window(QW.QMainWindow):
    def __init__(self, plate):
        super().__init__()
        self.plate = plate
        self.size = plate.size
        self.setWindowTitle("Cell Compute")
        self.setMinimumSize(500, 450)
        # Set central widget
        central_widget = QW.QWidget()
        self.setCentralWidget(central_widget)

        # Set high level layout
        self.base_layout = QW.QHBoxLayout(central_widget)
        self.input_layout = QW.QGridLayout()
        self.plate_layout = QW.QGridLayout()
        self.output_layout = QW.QGridLayout()
        self.side_panel_layout = QW.QVBoxLayout()
        self.base_layout.addLayout(self.input_layout, 1)
        self.base_layout.addLayout(self.plate_layout, 6)
        self.base_layout.addLayout(self.output_layout, 1)
        self.base_layout.addLayout(self.side_panel_layout, 2)
        self.plate_layout.setSpacing(0) 
        self.input_layout.setSpacing(0)
        self.output_layout.setSpacing(0)

        # Initialize widgets
        self.init_inputs()
        self.init_plate()
        self.init_outputs()
        self.init_side_panel()

    ## Initialization Methods ##
    def init_inputs(self):
        self.input_buttons = []
        for i in range(self.size):
            button = QW.QPushButton()
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            button.setStyleSheet("""
                    QPushButton {
                        background-color:lavender;
                        border: none;
                        margin: 1px;
                    }
                    """)
            button.clicked.connect(lambda checked, x=i: self.on_input_click(x))
            self.input_layout.addWidget(button, i, 0)
            self.input_buttons.append(button)

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
                            color: black;
                        }
                        """)
                button.clicked.connect(lambda checked, x=i, y=j: self.on_cell_click(x, y))
                self.plate_layout.addWidget(button, i, j)
                row.append(button)
            self.buttons.append(row)

    def init_outputs(self):
        self.output_buttons = []
        for i in range(self.size):
            button = QW.QPushButton()
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            button.setStyleSheet("""
                    QPushButton {
                        background-color:lavender;
                        border: none;
                        margin: 1px;
                        color: black;
                    }
                    """)
            self.output_layout.addWidget(button, i, 0)
            self.output_buttons.append(button)
        
    def init_side_panel(self):
        button_names = ["Set Input", "Randomize Plate", "Reset Plate", "Simulate"]
        button_functions = [self.on_set_input, self.on_randomize_plate_click, self.on_reset_click, self.on_simulate]
        
        # Add update button
        update_button = QW.QPushButton(button_names[0])
        update_button.clicked.connect(button_functions[0])
        self.side_panel_layout.addWidget(update_button)
        
        # Add percent NOR gates
        self.NOR_box_label = QW.QLabel("NOR gate percent:")
        self.side_panel_layout.addWidget(self.NOR_box_label)
        self.NOR_text_box = QW.QLineEdit("0.3")
        self.side_panel_layout.addWidget(self.NOR_text_box)
        # Add percent wire
        self.wire_box_label = QW.QLabel("Wire percent:")
        self.side_panel_layout.addWidget(self.wire_box_label)
        self.wire_text_box = QW.QLineEdit("0.5")
        self.side_panel_layout.addWidget(self.wire_text_box)

        # Add three buttons
        for i in range(1,3):
            button = QW.QPushButton(button_names[i])
            button.clicked.connect(button_functions[i])
            self.side_panel_layout.addWidget(button)

        # Add dropdown menu
        self.cell_type_label = QW.QLabel("Select Cell Type for Manual Entry:")
        self.side_panel_layout.addWidget(self.cell_type_label)
        self.cell_type_dropdown = QW.QComboBox()
        self.cell_type_dropdown.addItems(["empty", "wire", "nor"])
        self.side_panel_layout.addWidget(self.cell_type_dropdown)

        # Add stretch to push widgets to the top
        self.side_panel_layout.addStretch(1)
    
    ## Button Click Actions ##
    def on_input_click(self, x):
        button = self.input_buttons[x]
        current_state = button.text()

        if current_state == "":
            new_state = "0"
            color = "palevioletred"
        elif current_state == "0":
            new_state = "1"
            color = "darkcyan"
        else:
            new_state = ""
            color = "lavender"

        button.setText(new_state)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border: none;
                margin: 1px;
                color: black;
            }}
        """)

    def on_cell_click(self, x, y):
        selected_type = self.cell_type_dropdown.currentText()
        self.plate.add_cell(x, y, selected_type)
        self.update_cell_color(self.plate.active_cells[(x,y)])
        print(f'{x},{y}')
        
        
    def on_set_input(self):
        for i,button in enumerate(self.input_buttons):
            value = button.text()
            if value != "":
                value = int(value)
            else:
                value = -1
            self.plate.add_input(i, value)
        self.plate.update_plate()
        self.update_plate_colors()
        self.update_plate_text()
        outputs = self.plate.set_outputs()
        for i,button in enumerate(self.output_buttons):
            value = outputs[i]
            if value == -1:
                value = ''
            else:
                value = f'{value}'
            button.setText(value)

    def on_randomize_plate_click(self):
        """
        Warning: Running this will reset your plate!
        """
        NOR_percent = float(self.NOR_text_box.text())
        wire_percent = float(self.wire_text_box.text())
        self.update_plate_colors(reset=True)
        self.update_plate_text(reset=True)
        self.plate.randomize_plate(NOR_percent, wire_percent)
        self.update_plate_colors()

    def on_reset_click(self):
        for loc,cell in self.plate.get_active_cells().items():
            self.update_cell_color(cell, reset=True)
            self.update_plate_text(reset=True)
        self.plate.reset_plate()

    def on_simulate(self):
        inputs = self.plate.inputs

    ### Random helper fuctions
    def update_plate_text(self, reset=False):
        for loc,cell in self.plate.get_active_cells().items():
            button = self.buttons[cell.x][cell.y]
            if reset:
                button.setText('')
            else:
                if cell.value == -1:
                    button.setText('')
                else:
                    button.setText(f'{cell.value}')

    def update_plate_colors(self, reset=False):
        for loc,cell in self.plate.get_active_cells().items():
            self.update_cell_color(cell, reset=reset)

    def update_cell_color(self, cell, reset=False):
        button = self.buttons[cell.x][cell.y]
        color = colors["empty"] if reset else colors[cell.type]
        button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {color};
                        border: none;
                        margin: 1px;
                        color: black;   
                    }}
                """)

if __name__ == "__main__":
    plate = grid.Grid(50)
    app = QW.QApplication(sys.argv)
    window = Main_Window(plate)
    window.show()
    sys.exit(app.exec())
