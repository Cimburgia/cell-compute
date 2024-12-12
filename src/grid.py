import cell
import numpy as np

# Cell type dictionary
cell_type = [
    'empty',
    'wire',
    'nor',
    'c6_input',
    'c12_input']
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

    def add_cell(self, x, y, cell):
        self.grid_layout[x][y] = np.argwhere(cell_type == cell.type)
        self.active_cells[(cell.x, cell.y)] = cell

    def reset_plate(self):
        self.grid_layout = np.zeros((self.size, self.size))
        self.active_cells = {}

    def set_active_cells(self, layout):
        non_zero_indcies = np.argwhere(layout != 0)
        coordiantes = [(x,y) for x,y in non_zero_indcies]
  
        for x,y in coordiantes:
            cell_val = layout[x][y]
            new_cell = cell.Cell(x, y, cell_type[int(cell_val)])
            self.active_cells[(x,y)] = new_cell

    def get_active_cells(self):
        return self.active_cells
    
    def randomize_plate(self, percent_nor_fill=0.2, percent_wire_fill=0.5,):
        """
        This function will randomize the plate with either exclusively nor gates at a
        certain percentage or both wires and nor gates. This function will be used for
        running simulations.

        Warning: Running this will reset your plate!
        """
        self.reset_plate()
        total_cells = self.size ** 2
        num_nor_gates = int(total_cells * percent_nor_fill)
        num_wires = int(total_cells * percent_wire_fill)

        plate_array = self.grid_layout.flatten()
        indicies = np.random.choice(total_cells, num_nor_gates + num_wires, replace=False)
        for i,j in enumerate(indicies):
            if i <= num_wires:
                plate_array[j] = 1
            else:
                plate_array[j] = 2

        plate_2d = plate_array.reshape(self.size, self.size)
        self.grid_layout = plate_2d
        self.set_active_cells(self.grid_layout)



if __name__ == "__main__":
    grid = Grid(10)
    grid.show_grid()