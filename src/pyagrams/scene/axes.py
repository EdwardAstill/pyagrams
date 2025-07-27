"""
Axes class - Container for coordinate systems and primitives
"""
from ..core.geometry2d import Spline, Point, Vector


class Axes:
    def __init__(self, position=None, size=None):
        self.position = position or [0, 0]  # (x, y) position within diagram
        self.size = size or [10, 10]
        self.objects = []  # Store primitives (points, lines, etc.) in order of addition
        self.thickness = 1
        self.color = "gray"
        self.line_style = "dashed"  # Default to dashed lines
        
        # Create two vectors for x and y axes
        self.x_vector = Vector(self.position, [self.size[0], 0])
        self.y_vector = Vector(self.position, [0, self.size[1]])
        self._update_vector_styles()
    
    def _update_vector_styles(self):
        """Update vector styles to match axes settings"""
        for vector in [self.x_vector, self.y_vector]:
            vector.style.color = self.color
            vector.style.thickness = self.thickness
            vector.style.line_style = self.line_style
    
    def size(self, width, height):
        """Set axes size"""
        self.size = [width, height]
        # Update vector directions
        self.x_vector.direction = [width, 0]
        self.y_vector.direction = [0, height]
        return self
    
    def position(self, x, y):
        """Set axes position"""
        self.position = [x, y]
        # Update vector positions
        self.x_vector.position = [x, y]
        self.y_vector.position = [x, y]
        return self
    
    def style(self, line_style):
        """Set axes line style: 'dashed' or 'solid'"""
        if line_style not in ("dashed", "solid"):
            raise ValueError("line_style must be 'dashed' or 'solid'")
        self.line_style = line_style
        self._update_vector_styles()
        return self
    
    def add_point(self, size, coords):
        """Add a point to the axes at the given coordinates (relative to axes origin)"""
        # Transform relative coordinates to absolute coordinates by adding axes origin
        absolute_coords = [
            self.position[0] + coords[0],
            self.position[1] + coords[1]
        ]
        self.objects.append(("point", size, absolute_coords))
        return self
    
    def add_vector(self, relative_position, direction):
        """Add a vector to the axes with position relative to axes origin"""
        # Convert relative position to absolute position by adding axes origin
        absolute_position = [
            self.position[0] + relative_position[0],
            self.position[1] + relative_position[1]
        ]
        # Store as vector object in objects list
        vector = Vector(absolute_position, direction)
        vector.style.line_style = "solid"  # Override default dashed style for axes vectors
        self.objects.append(("vector", vector))
        return vector
    
    def add_spline(self, spline):
        """Add a spline whose points are *relative* to this axes origin."""
        abs_pts = [[self.position[0] + p[0],
                    self.position[1] + p[1]] for p in spline.points]
        spline.points = abs_pts                # now absolute
        self.objects.append(("spline", spline))
        return spline

    def add_object(self, obj):
        """Generic method to add any object to the axes. 
        Automatically determines the object type and calls the appropriate specific method."""
        if isinstance(obj, Point):
            # Create a new point with the same properties but adjusted coordinates
            absolute_coords = [
                self.position[0] + obj.coords[0],
                self.position[1] + obj.coords[1]
            ]
            new_point = Point(obj.size, absolute_coords)
            # Copy label and style from original object
            if obj.label:
                new_point.set_label(obj.label, obj.label_position)
            new_point.style = obj.style
            self.objects.append(("point", new_point))
            return new_point
        elif isinstance(obj, Vector):
            # For vectors, the position should already be relative to axes origin
            # So we just need to convert it to absolute by adding axes origin
            absolute_position = [
                self.position[0] + obj.position[0],
                self.position[1] + obj.position[1]
            ]
            # Create a new vector with absolute position
            new_vector = Vector(absolute_position, obj.direction)
            # Copy label and style from original object
            if obj.label:
                new_vector.set_label(obj.label, obj.label_position)
            new_vector.style = obj.style
            new_vector.style.line_style = "solid"  # Override default dashed style for axes vectors
            self.objects.append(("vector", new_vector))
            return new_vector
        elif isinstance(obj, Spline):
            # Create a copy of the spline with adjusted points
            abs_pts = [[self.position[0] + p[0],
                        self.position[1] + p[1]] for p in obj.points]
            new_spline = Spline(abs_pts, obj.tangents)
            # Copy label and style from original object
            if obj.label:
                new_spline.set_label(obj.label, obj.label_position)
            new_spline.style = obj.style
            self.objects.append(("spline", new_spline))
            return new_spline
        else:
            raise TypeError(f"Unsupported object type: {type(obj)}. "
                          f"Supported types are Point, Vector, and Spline.")

    def add_to(self, diagram):
        """Add this axes to a diagram"""
        diagram.add_axes(self)
        return self

    def add_ticks(self, spacing, length=5, color="black", orientation="both", placement="inside"):
        """Add ticks to the axes. 
        orientation: 'x', 'y', or 'both'
        placement: 'inside', 'outside', or 'middle'
        """
        ox, oy = self.position
        if orientation in ("x", "both"):
            for i in range(spacing, self.size[0]+1, spacing):
                # x-axis ticks: vertical lines at the axis
                if placement == "inside":
                    start, end = [ox+i, oy], [ox+i, oy+length]
                elif placement == "outside":
                    start, end = [ox+i, oy], [ox+i, oy-length]
                elif placement == "middle":
                    start, end = [ox+i, oy-length/2], [ox+i, oy+length/2]
                else:
                    raise ValueError("placement must be 'inside', 'outside', or 'middle'")
                self.objects.append(("tick", start, end, color))
        if orientation in ("y", "both"):
            for i in range(spacing, self.size[1]+1, spacing):
                # y-axis ticks: horizontal lines at the axis
                if placement == "inside":
                    start, end = [ox, oy+i], [ox+length, oy+i]
                elif placement == "outside":
                    start, end = [ox, oy+i], [ox-length, oy+i]
                elif placement == "middle":
                    start, end = [ox-length/2, oy+i], [ox+length/2, oy+i]
                else:
                    raise ValueError("placement must be 'inside', 'outside', or 'middle'")
                self.objects.append(("tick", start, end, color))
        return self
    
    def addPoint(self, size, coords):
        """Add point to axes (compatibility method)"""
        return self.add_point(size, coords)
    
    def addLine(self, start, end):
        """Add line to axes (compatibility method - creates a vector)"""
        direction = [end[0] - start[0], end[1] - start[1]]
        return self.add_vector(start, direction) 