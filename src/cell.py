
# Cell class
class Cell:
    """
    
    """
    def __init__(self, x, y, type="empty"):
        self.type = type
        self.x = x
        self.y = y
        self.density = 0
        self.c6_conc = 0.0
        self.c12_conc = 0.0
        self.c5_conc = 0.0
        self.c6_prod_rate = 0.0
        self.c12_prod_rate = 0.0
        self.c5_prod_rate = 0.0
    
    def update(self):
        pass

    def get_neighbors(self, x, y, size, radius=1):
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < size and 0 <= ny < size:
                    neighbors.append((nx, ny))
        return neighbors

    
if __name__ == "__main__":
    print("todo")