class Vector:
    def __init__(self, x : int = 0, y : int = 0):
        self.x = x
        self.y = y

    
    def setVec(self, v):
        self.x = v.x
        self.y = v.y

    
    def compareVec(self, x, y):
        return self.x == x and self.y == y
    
    
    def to_cords(self):
        return self.x, self.y

    
    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        elif isinstance(other, tuple):
            return Vector(self.x + other[0], self.y + other[1])
        else:
            return TypeError('Unsupported type')