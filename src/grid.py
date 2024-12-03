import cell
import numpy as np

# Cell type dictionary
cell_type = {
    'empty':0,
    'wire':1,
    'nor':2,
    'c6_input':3,
    'c12_input':4
}
# Grid class
class Grid:
    """
    
    """
    def __init__(self, size):
        self.size = size
        self.grid_layout = np.zeros((size, size))
        self.active_cells = {}

    def show_grid(self):
        print(self.grid_layout)   

    def get_neighbors(self, x, y):
        pass

    def add_cell(self, x, y, cell):
        self.grid_layout[x][y] = cell_type[cell.type]
        self.active_cells[(cell.x, cell.y)] = cell

    def reset_plate(self):
        self.grid_layout = np.zeros((self.size, self.size))


if __name__ == "__main__":
    grid = Grid(10)
    grid.show_grid()