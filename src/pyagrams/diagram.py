"""
Diagram class - Container for axes and primitives within a figure
"""
import numpy as np
from .axis_objects import Spline, Point, Vector
        


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
            vector.color = self.color
            vector.thickness = self.thickness
            vector.line_style = self.line_style
    
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
        vector.line_style = "solid"  # Override default dashed style for axes vectors
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
            return self.add_point(obj.size, obj.coords)
        elif isinstance(obj, Vector):
            # For vectors, we need to convert absolute position to relative
            relative_position = [
                obj.position[0] - self.position[0],
                obj.position[1] - self.position[1]
            ]
            return self.add_vector(relative_position, obj.direction)
        elif isinstance(obj, Spline):
            return self.add_spline(obj)
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

    def to_svg(self, diagram_width, diagram_height):
        """Generate SVG representation of the axes and its elements"""
        svg_parts = []
        
        # Update vector styles before rendering
        self._update_vector_styles()
        
        # Render x and y vectors
        svg_parts.append(self.x_vector.to_svg(diagram_width, diagram_height))
        svg_parts.append(self.y_vector.to_svg(diagram_width, diagram_height))

        # Render all objects in order
        for obj in self.objects:
            if obj[0] == "point":
                _, size, coords = obj
                # Convert coordinates to SVG space
                svg_y = diagram_height - coords[1]
                svg_x = coords[0]
                svg_parts.append(f'<circle cx="{svg_x}" cy="{svg_y}" r="{size/2}" fill="black"/>')
            elif obj[0] == "vector":
                _, vector = obj
                svg_parts.append(vector.to_svg(diagram_width, diagram_height))
            elif obj[0] == "tick":
                _, start, end, color = obj
                # Apply coordinate transformation 
                tick_start_x = start[0]
                tick_start_y = diagram_height - start[1]
                tick_end_x = end[0]
                tick_end_y = diagram_height - end[1]
                svg_parts.append(f'<line x1="{tick_start_x}" y1="{tick_start_y}" x2="{tick_end_x}" y2="{tick_end_y}" stroke="{color}" stroke-width="1"/>')
            elif obj[0] == "spline":
                _, spline = obj
                svg_parts.append(spline.to_svg(diagram_width, diagram_height))
        
        return '\n'.join(svg_parts)


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
        vector.line_style = "solid"  # Override default dashed style for diagram vectors
        self._vectors.append(vector)
        return vector
    
    
    def to_svg(self):
        """Generate SVG representation of the diagram"""
        svg_parts = []
        
        # Calculate y position from bottom if figure reference is available
        if self.figure:
            # y is distance from bottom, so convert to distance from top
            y_from_top = self.figure._height - self.height - self.y
            print(f"Debug: figure height={self.figure._height}, diagram height={self.height}, y={self.y}, y_from_top={y_from_top}")
        else:
            y_from_top = self.y
            print(f"Debug: no figure reference, using y={self.y}")
        
        # Create a group for this diagram
        svg_parts.append(f'<g transform="translate({self.x},{y_from_top})">')
        
        # Diagram outline (black border for visibility)
        fill_value = self._fill if self._fill_enabled else "none"
        svg_parts.append(f'<rect width="{self.width}" height="{self.height}" '
                       f'fill="{fill_value}" stroke="black" stroke-width="2"/>')
        
        # Render points
        for px, py, psize in self._points:
            # SVG y=0 is top, so invert y for correct placement within the diagram
            svg_y = self.height - py
            svg_x = px
            svg_parts.append(f'<circle cx="{svg_x}" cy="{svg_y}" r="{psize/2}" fill="black"/>')

        # Render vectors
        for vector in self._vectors:
            svg_parts.append(vector.to_svg(self.width, self.height))

        # Render axes
        for axes in self.axes:
            svg_parts.append(axes.to_svg(self.width, self.height))
         
        svg_parts.append('</g>')
        
        return '\n'.join(svg_parts) 

from .axis_objects import Spline
