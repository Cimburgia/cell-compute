import tkinter as tk
from tkinter import ttk
import cell
import grid

colors = {
    "wire":"green",
    "nor":"SlateBlue1",
    "empty":"light yellow"
}

class Window:
    def __init__(self, plate):
        self.size = plate.size
        self.window = tk.Tk()
        self.window.title(f"Cell Compute")
        self.window.geometry("700x500")
        # Window Layout
        self.window.grid_columnconfigure(0, weight=4)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        # Frames
        self.grid_frame = tk.Frame(self.window)
        self.grid_frame.grid(row=0, column=0, sticky="nsew")
        self.side_frame = tk.Frame(self.window)
        self.side_frame.grid(row=0, column=1, sticky="nsew", padx=10)
        # Initialize
        self.init_plate()
        self.init_side_frame()
        self.set_square_window()
        # Create grid object
        self.plate = plate

    def init_plate(self):
        """
        Initializes an empty plate to place a pattern. Each cell will be blank until updated
        """
        self.buttons = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                button = tk.Button(self.grid_frame, bg=colors["empty"])
                button.grid(row=i, column=j, sticky="nsew")
                button.bind("<Button-1>", lambda event, x=i, y=j: self.cell_on_click(x, y))
                row.append(button)
            self.buttons.append(row)

    def init_side_frame(self):
        """
        Initializes the side frame with five buttons and a text area
        """
        self.side_frame.grid_columnconfigure(0, weight=1)
        button_names = ["Update Plate", "Button 2", "Button 3", "Button 4", "Button 5"]
        button_funtions = [self.update_on_click, self.button2_function, self.button3_function, self.button4_function, self.button5_function]
        for i, name in enumerate(button_names):
            button = tk.Button(self.side_frame, text=name, command=button_funtions[i])
            button.grid(row=i, column=0, pady=5, sticky="ew")
        # Menu Choice and combobox
        cell_types = ["empty", "wire", "nor"]
        self.cell_type_var = tk.StringVar(self.side_frame)
        self.combobox_cell_type = ttk.Combobox(
            self.side_frame, 
            textvariable=self.cell_type_var,
            values=cell_types,
            state="readonly"
        )
        self.combobox_cell_type.set(cell_types[0])
        self.side_frame.grid_rowconfigure(len(button_names), weight=1)
        self.combobox_cell_type.grid(row=len(button_names), column=0, pady=0, sticky="new")

    
    def set_square_window(self):
        """
        Used to format the grid frame so that it scales with window size
        """
        for i in range(self.size):
            self.grid_frame.grid_rowconfigure(i, weight=1)
            self.grid_frame.grid_columnconfigure(i, weight=1)

    def cell_on_click(self, x, y):
        """
        Action when button is clicked.
        """
        selected_type = self.cell_type_var.get()
        new_cell = cell.Cell(x, y, type=selected_type)
        self.plate.add_cell(x, y, new_cell)

        button = self.buttons[x][y]
        button.config(
            bg=colors[selected_type]
        )
        button.update()



    def update_on_click(self):
        print(self.plate.show_grid())

    def button2_function():
        print("Button 2 clicked")

    def button3_function():
        print("Button 3 clicked")

    def button4_function():
        print("Button 4 clicked")

    def button5_function():
        print("Button 5 clicked")

    def update_color(self):
        pass

    def run(self):
        """
        Starts the main application
        """
        self.window.mainloop()

if __name__ == "__main__":
    plate = grid.Grid(15)
    app = Window(plate)
    app.run()
