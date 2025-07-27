"""
Diagram class - Container for axes and visual elements within a figure
"""
from .axes import Axes
from ..core.geometry2d import Vector


class Diagram:
    def __init__(self, width=200, height=200, x=0, y=0, figure=None):
        self.width = width
        self.height = height
        self.x = x  # Position within figure
        self.y = y  # Position within figure (from bottom-left if figure provided)
        self.figure = figure  # Reference to parent figure for bottom-relative positioning
        self.axes = []
        self._fill = "none"  # Default: no fill
        self._fill_enabled = False
        self._points = []  # Store points as (x, y, size) tuples
        self._vectors = []  # Store vectors separately
    
    def size(self, width, height):
        """Set diagram dimensions"""
        self.width = width
        self.height = height
        return self
    
    def position(self, x, y):
        """Set diagram position within figure"""
        self.x = x
        self.y = y
        return self
    
    def fill(self, color=None):
        """Set fill color for the diagram. If color is None, disables fill."""
        if color is None:
            self._fill_enabled = False
            self._fill = "none"
        else:
            self._fill_enabled = True
            self._fill = color
        return self
    
    def add_point(self, *args):
        """Add a point to the diagram. Accepts (x, y, size) or ([x, y], size)."""
        if len(args) == 3:
            x, y, size = args
        elif len(args) == 2 and isinstance(args[0], (list, tuple)):
            (x, y), size = args
        else:
            raise TypeError("add_point expects (x, y, size) or ([x, y], size)")
        self._points.append((x, y, size))
        return self

    def add_axes(self, axes_or_position, size=None):
        """Add a set of axes to the diagram. Can accept either an Axes object or position/size parameters"""
        if isinstance(axes_or_position, Axes):
            # If an Axes object is passed, just add it
            self.axes.append(axes_or_position)
            return axes_or_position
        else:
            # If position and size are passed, create new Axes
            axes = Axes(axes_or_position, size)
            self.axes.append(axes)
            return axes
    
    def add_vector(self, position=None, direction=None):
        """Add a vector to the diagram. Vectors default to solid when added to diagram.
        Can accept either a Vector object or position/direction parameters."""
        if isinstance(position, Vector):
            # If a Vector object is passed as the first argument, use it directly
            vector = position
        else:
            # Otherwise create a new Vector with position and direction
            vector = Vector(position, direction)
        vector.style.line_style = "solid"  # Override default dashed style for diagram vectors
        self._vectors.append(vector)
        return vector
    
    def addAxes(self, position, size=None):
        """Add axes to diagram (compatibility method)"""
        return self.add_axes(position, size)
    
    def addPoint(self, size, coords):
        """Add point to diagram (compatibility method)"""
        return self.add_point(coords[0], coords[1], size)
    
    def addLine(self, start, end):
        """Add line to diagram (compatibility method - creates a vector)"""
        direction = [end[0] - start[0], end[1] - start[1]]
        return self.add_vector(start, direction) 