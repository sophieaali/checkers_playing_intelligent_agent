class Location:
    """
    The Location class is used to represent a location on the board. It is used to represent the location of a piece on the board.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Location(x={self.x}, y={self.y})"