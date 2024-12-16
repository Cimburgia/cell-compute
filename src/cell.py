import numpy as np
import random 
# Cell class
class Cell:
    """
    
    """
    def __init__(self, x, y, type="empty", value=-1):
        self.type = type
        self.value = value
        self.x = x
        self.y = y
        self.density = 0
        self.c6_conc = 0.0
        self.c12_conc = 0.0
        self.c6_prod_rate = 0.0
        self.c12_prod_rate = 0.0
        self.input_weights = [.5, 1, .5]

    
    def get_previous(self, plate_size, start=False):
        if self.x == 0:
            dx = [0, 1]
        elif self.x == plate_size - 1:
            dx = [-1, 0]
        else:
            dx = [-1, 0, 1]
        ny = self.y - 1
        if start:
            prev = [self.x + nx for nx in dx]
        else:
            prev = [(self.x + nx, ny) for nx in dx]
        return prev


    def get_neighbors(self, size, radius=1):
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < size and 0 <= ny < size:
                    neighbors.append((nx, ny))
        return neighbors

    def update(self, values, size):
        first_cell = self.x < 1
        last_cell = self.x == size - 1
        if self.type == "wire":
            new_val = self.wire_update(values, first_cell, last_cell)
        elif self.type == "nor":
            new_val = self.nor_update(values)
        self.value = new_val
        return new_val
    
    def wire_update(self, values, first_cell, last_cell):
        # Case 1: Direct cell back has signal
        nn = 0 if first_cell else 1
        if values[nn] >= 0:
            new_value = values[nn]
        # Case 2: Direct cell is empty
        elif values[nn] < 0:
            if first_cell:
                new_value = values[1]
            elif last_cell:
                new_value = values[0]
            else:
                if values[0] == values[2]:
                    new_value = values[0]
                elif values[0] < 0:
                    new_value = values[2]
                elif values[2] < 0:
                    new_value = values[0]
                else:
                    # Make deterministic for now
                    new_value = np.max([values[0], values[2]])
        return new_value        
            
    def nor_update(self, values):
        if 1 in values:
            new_value = 0
        elif 0 in values and 1 not in values:
            new_value = 1
        else:
            new_value = -1
        return new_value
    
if __name__ == "__main__":
    print("todo")