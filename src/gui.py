import tkinter as tk

class Window:
    def __init__(self, size):
        self.size = size
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

    def init_plate(self):
        """
        Initializes an empty plate to place a pattern. Each cell will be blank until updated
        """
        self.buttons = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                button = tk.Button(self.grid_frame, text=f"({i},{j})")
                button.grid(row=i, column=j, sticky="nsew")
                button.bind("<Button-1>", lambda event, x=i, y=j: self.on_click(x, y))
                row.append(button)
            self.buttons.append(row)

    def init_side_frame(self):
        """
        Initializes the side frame with five buttons and a text area
        """
        self.side_frame.grid_columnconfigure(0, weight=1)
        button_names = ["Button 1", "Button 2", "Button 3", "Button 4", "Button 5"]
        for i, name in enumerate(button_names):
            button = tk.Button(self.side_frame, text=name)
            button.grid(row=i, column=0, pady=5, sticky="ew")
        self.text_area = tk.Text(self.side_frame, width=20, height=10)
        self.text_area.grid(row=len(button_names), column=0, pady=10, sticky="nsew")
        self.side_frame.grid_rowconfigure(len(button_names), weight=1)


    def set_square_window(self):
        """
        Used to format the grid frame so that it scales with window size
        """
        for i in range(self.size):
            self.grid_frame.grid_rowconfigure(i, weight=1)
            self.grid_frame.grid_columnconfigure(i, weight=1)

    def on_click(self, x, y):
        """
        Action when button is clicked.
        """
        print(f"Clicked button at ({x},{y})")

    def run(self):
        """
        Starts the main application
        """
        self.window.mainloop()

if __name__ == "__main__":
    grid_size = 4
    app = Window(grid_size)
    app.run()
