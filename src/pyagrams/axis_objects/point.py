"""
Point class - Container for a point with x, y, size, and color
"""
class Point:
    """
    Point class - Container for a point with x, y, size, and color
    add a point to axis bu doing axes.addPoint(Point(x, y, size))
    or Point(x, y, size).add_to(axes)
    """
    def __init__(self, size, coords):
        self.coords = coords
        self.size = size
        self.color = "black"
    
    def add_to(self, axes):
        """Add the point to the axes"""
        axes.addPoint(self.size, self.coords)
        return self 