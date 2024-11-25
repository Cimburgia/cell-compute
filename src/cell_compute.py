import tkinter as tk

# Initialize the main window
root = tk.Tk()
root.title("Cell Compute")

# Define grid dimensions and colors and parameters
grid_size = 12
square_size = 30
default_color = "light yellow"
colors = ["dark red", "green", "powder blue", "SlateBlue1", "light yellow"]
cellStates = ["C6 input", "C12 input", "Bioink WIRE", "Bioink NOR", "No Cells"]

growthFactor = 0.1
diffusionFactor = 0.2
productionFactor = 0.1

# Define cell parameters with default or initial random values
class Cell:
    def __init__(self):
        self.state = "No Cells"
        self.cellDensity = 0.0
        self.growthRate = 0.0
        self.C6conc = 0.0
        self.C12conc = 0.0
        self.C5conc = 0.0
        self.C6prodRate = 0.0
        self.C12prodRate = 0.0
        self.C5prodRate = 0.0
        self.color = "light yellow"
        self.neighbors = []

# Function to update the selected cell state when a button is clicked
def select_state(state):
    global selected_state
    selected_state = state

# Function to display parameters inside each square
def display_parameters():
    for row in range(grid_size):
        for col in range(grid_size):
            cell = cell_grid[row][col]
            if cell.cellDensity > 0.0:
                text = f"D:{cell.cellDensity:.2f}\nc6:{cell.C6conc:.2f}\nc12:{cell.C12conc:.2f}\nc5:{cell.C5conc:.2f}"
            else:
                text = ''    
            grid_labels[row][col].config(text=text)


def getColor(state):
    for i, s in enumerate(cellStates):
        if s == state:
            return colors[i]

# Function to change the color of a clicked square
def change_state(event):
    event.widget.config(bg=getColor(selected_state))
    row, col = event.widget.grid_info()["row"], event.widget.grid_info()["column"]
    cell = cell_grid[row][col]

    if selected_state == "C6 input":
        cell.state, cell.cellDensity, cell.C6conc, cell.C6prodRate = cellStates[0], 1.0, 1.0, 1.0
        cell.C12conc, cell.C12prodRate, cell.C5conc, cell.C5prodRate = 0.0, 0.0, 0.0, 0.0
    elif selected_state == "C12 input":
        cell.state, cell.cellDensity, cell.C12conc, cell.C12prodRate = cellStates[1], 1.0, 1.0, 1.0
        cell.C6conc, cell.C6prodRate, cell.C5conc, cell.C5prodRate = 0.0, 0.0, 0.0, 0.0
    elif selected_state == "Bioink WIRE":
        cell.state, cell.cellDensity = cellStates[2], 0.1
    elif selected_state == "Bioink NOR":
        cell.state, cell.cellDensity = cellStates[3], 0.1
    else:
        cell.state, cell.cellDensity, cell.C6conc, cell.C12conc, cell.C5conc = cellStates[4], 0.0, 0.0, 0.0, 0.0

# Precompute and cache neighbors for each cell
def initialize_neighbors():
    for row in range(grid_size):
        for col in range(grid_size):
            neighbors = []
            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    if 0 <= r < grid_size and 0 <= c < grid_size and (r != row or c != col):
                        neighbors.append(cell_grid[r][c])
            cell_grid[row][col].neighbors = neighbors

# Function to update Bioink cells based on neighboring cells' parameters
def update_bioink():
    for row in range(grid_size):
        for col in range(grid_size):
            cell = cell_grid[row][col]
            square_label = grid_labels[row][col]

            if cell.state == "Bioink WIRE" or cell.state == "Bioink NOR":
                neighbors = cell.neighbors
                cell.cellDensity += (1 - cell.cellDensity) * cell.growthRate
                cell.growthRate = ((cell.C6conc + cell.C12conc + cell.C5conc)/3 if cell.state == "Bioink NOR" else abs(cell.C6conc - cell.C12conc)) * growthFactor

                # Aggregate diffusion calculations
                cell.C6conc += max(0, cell.cellDensity * (1 - cell.C6conc) * (sum(n.C6prodRate for n in neighbors) / len(neighbors))) * diffusionFactor
                cell.C12conc += max(0, cell.cellDensity * (1 - cell.C12conc) * (sum(n.C12prodRate for n in neighbors) / len(neighbors))) * diffusionFactor
                cell.C5conc += max(0, cell.cellDensity * (1 - cell.C5conc) * (sum(n.C5prodRate for n in neighbors) / len(neighbors))) * diffusionFactor

                # Production calculations
                if cell.state == "Bioink WIRE":
                    cell.C6prodRate += cell.cellDensity * (cell.C6conc - cell.C12conc) * productionFactor
                    cell.C12prodRate += cell.cellDensity * (cell.C12conc + cell.C5conc - cell.C6conc) * productionFactor
                elif cell.state == "Bioink NOR":
                    cell.C6prodRate += cell.cellDensity * cell.C12conc * productionFactor
                    cell.C5prodRate += cell.cellDensity * (cell.C5conc + cell.C6conc - cell.C12conc**2) * productionFactor

                # Optional: Change color intensity based on cell parameters
                square_label.config(bg=getColorBasedOnConcentration(cell))
    display_parameters()


def getColorBasedOnConcentration(cell):
    """ Determine color based on C6conc, C12conc, and C5conc values """
    if  cell.state == "Bioink NOR":
        RGvals = int(255-cell.C5conc*255)
        return f'#{RGvals:02x}{RGvals:02x}ff'
    elif cell.C6conc > cell.C12conc:
        GBvals = int(255-cell.C6conc*255)
        return f'#ff{GBvals:02x}{GBvals:02x}'
    elif cell.C6conc <= cell.C12conc:
        RBvals = int(255-cell.C12conc*255)
        return f'#{RBvals:02x}ff{RBvals:02x}'

def update_bioink10():
    for _ in range(10):
        update_bioink()

def resetPlate():
    for row in range(grid_size):
        for col in range(grid_size):
            cell_grid[row][col].state = cellStates[4]
            cell_grid[row][col].cellDensity = cell_grid[row][col].growthRate = cell_grid[row][col].C6conc = cell_grid[row][col].C12conc = cell_grid[row][col].C5conc = 0.0
            grid_labels[row][col].config(bg=colors[4])
    display_parameters()

# Initialize Tkinter frames and grid layout
grid_frame = tk.Frame(root)
grid_frame.grid(row=0, column=0, padx=10, pady=10)
button_frame = tk.Frame(root)
button_frame.grid(row=0, column=1, padx=10, pady=10)

selected_state = "No Cells"
cell_grid = []
grid_labels = []
ink_cells = []
for row in range(grid_size):
    row_cells = []
    row_labels = []
    for col in range(grid_size):
        cell = Cell()
        square = tk.Label(grid_frame, bg=default_color, fg='#000000', width=6, height=4, relief="solid")
        square.grid(row=row, column=col)
        square.bind("<Button-1>", change_state)
        row_cells.append(cell)
        row_labels.append(square)
    cell_grid.append(row_cells)
    grid_labels.append(row_labels)

initialize_neighbors()
display_parameters()

# Create color selection buttons
for idx, state in enumerate(cellStates):
    button = tk.Button(button_frame, text=state.capitalize(), bg=colors[idx], command=lambda s=state: select_state(s))
    button.pack(pady=5)

# Create update and reset buttons
update_button = tk.Button(button_frame, text="Update Bioink Cells", command=update_bioink)
update_button.pack(pady=10)
update10_button = tk.Button(button_frame, text="Update Bioink Cells 10x", command=update_bioink10)
update10_button.pack(pady=10)
reset_button = tk.Button(button_frame, text="Reset Plate", command=resetPlate)
reset_button.pack(pady=10)

# Run the Tkinter main loop
root.mainloop()
