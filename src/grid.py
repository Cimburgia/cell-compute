import cell
import numpy as np
import heapq

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
    The grid is the representation of the plate that will grow colonies of E.coli
    """
    def __init__(self, size):
        self.size = size
        self.inputs = np.full(size, -1)
        self.grid_layout = np.zeros((size, size), dtype=int)
        self.grid_values = np.full((size, size), -1)
        self.outputs = np.full(size, -1)
        self.active_cells = {}

    def show_grid(self):
        print(self.grid_layout)   

    def add_input(self, x, val):
        self.inputs[x] = val

    def add_cell(self, x, y, type):
        new_cell = cell.Cell(x,y,type)
        self.grid_layout[x][y] = cell_type.index(type)
        self.active_cells[(x, y)] = new_cell

    def reset_plate(self):
        self.grid_layout = np.zeros((self.size, self.size))
        self.active_cells = {}

    def reset_plate_values(self):
        self.grid_values = np.full((self.size, self.size), -1)

    def set_active_cells(self):
        non_zero_indcies = np.argwhere(self.grid_layout != 0)
        coordiantes = [(x,y) for x,y in non_zero_indcies]
  
        for x,y in coordiantes:
            cell_val = self.grid_layout[x][y]
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
            if i < num_wires:
                plate_array[j] = 1
            else:
                plate_array[j] = 2

        plate_2d = plate_array.reshape(self.size, self.size)
        self.grid_layout = plate_2d
        self.set_active_cells()

    def get_prev_values(self, cell):
        start = cell.y < 1
        prev = cell.get_previous(self.size, start)
        if start:
            prev_values = [int(self.inputs[p]) for p in prev]
        else:
            prev_values = [int(self.grid_values[p[0]][p[1]]) for p in prev]
        return prev_values
        
    def update_col(self, col_number):
        for row in range(self.size):
            if (row, col_number) in self.active_cells.keys():
                cell = self.active_cells[(row, col_number)]
                prev_values = self.get_prev_values(cell)
                new_val = cell.update(prev_values, self.size)
                self.grid_values[row][col_number] = new_val

    def update_plate(self):
        self.set_active_cells()
        for col in range(self.size):
            self.update_col(col)

    def set_outputs(self):
        self.outputs = self.grid_values[:,-1]
        return self.outputs


        

if __name__ == "__main__":
    grid = Grid(50)
    grid.show_grid()