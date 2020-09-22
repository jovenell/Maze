class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.top_wall = True
        self.bottom_wall = True
        self.left_wall = True
        self.right_wall = True
        self.value = 0
        self.dist_from_start = 0
        self.dist_to_end = 0
        self.parent = None