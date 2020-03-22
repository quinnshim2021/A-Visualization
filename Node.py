class Node:
    def __init__(self, parent, position):
        self.position = position
        self.parent = parent

        self.g = 0
        self.h = 0
        self.f = 0
    
    def __eq__(self, comparator):
        if self.position[0] == comparator.position[0] and self.position[1] == comparator.position[1]:
            return True