"""
Diagram class - Container for axes and primitives within a figure
"""
import numpy as np

class Vector:
    """
    Vector class - A line with arrow tip defined by position and direction vectors
    """
    def __init__(self, position=None, direction=None):
        self.position = position or [0, 0]  # Starting point of the vector
        self.direction = direction or [10, 10]  # Direction and magnitude
        self.color = "gray"
        self.thickness = 1
        self.line_style = "dashed"  # 'dashed' or 'solid'
        self.arrow_size = 8  # Size of arrow tip (increased from 5)
        
    def style(self, line_style):
        """Set vector line style: 'dashed' or 'solid'"""
        if line_style not in ("dashed", "solid"):
            raise ValueError("line_style must be 'dashed' or 'solid'")
        self.line_style = line_style
        return self
        
    def color(self, color):
        """Set vector color"""
        self.color = color
        return self
        
    def thickness(self, thickness):
        """Set vector thickness"""
        self.thickness = thickness
        return self
        
    def to_svg(self, diagram_width, diagram_height):
        """Generate SVG representation of the vector"""
        svg_parts = []
        
        # Calculate end point
        start_x, start_y = self.position
        end_x = start_x + self.direction[0]
        end_y = start_y + self.direction[1]
        
        # Convert to SVG coordinates (y=0 is top)
        svg_start_y = diagram_height - start_y
        svg_end_y = diagram_height - end_y
        
        # Determine stroke-dasharray based on line style
        dash_length = 8
        dash_gap = 2
        dash_array = f"{dash_length},{dash_gap}" if self.line_style == "dashed" else "none"
        
        # Draw main line
        svg_parts.append(f'<line x1="{start_x}" y1="{svg_start_y}" x2="{end_x}" y2="{svg_end_y}" '
                        f'stroke="{self.color}" stroke-width="{self.thickness}" stroke-dasharray="{dash_array}" '
                        f'stroke-linecap="round"/>')
        
        # Calculate arrow tip
        if self.direction[0] != 0 or self.direction[1] != 0:
            # Vector direction angle
            angle = np.arctan2(self.direction[1], self.direction[0])
            
            # Arrow tip angles (20 degrees on each side for narrower tips)
            arrow_angle = np.pi / 9  # 20 degrees (reduced from 30)
            
            # Calculate arrow tip points
            arrow1_x = end_x - self.arrow_size * np.cos(angle - arrow_angle)
            arrow1_y = end_y - self.arrow_size * np.sin(angle - arrow_angle)
            svg_arrow1_y = diagram_height - arrow1_y
            
            arrow2_x = end_x - self.arrow_size * np.cos(angle + arrow_angle)
            arrow2_y = end_y - self.arrow_size * np.sin(angle + arrow_angle)
            svg_arrow2_y = diagram_height - arrow2_y
            
            # Draw a small line from tip back along vector to fill dash gap
            if self.line_style == "dashed":
                # Gap fill line should be exactly the length of the dash gap
                gap_fill_length = dash_gap
                gap_fill_end_x = end_x - gap_fill_length * np.cos(angle)
                gap_fill_end_y = end_y - gap_fill_length * np.sin(angle)
                svg_gap_fill_end_y = diagram_height - gap_fill_end_y
                
                svg_parts.append(f'<line x1="{end_x}" y1="{svg_end_y}" x2="{gap_fill_end_x}" y2="{svg_gap_fill_end_y}" '
                               f'stroke="{self.color}" stroke-width="{self.thickness}"/>')
            
            # Draw arrow tip as curved arcs with round linecaps
            # Create a curved arrow tip using SVG path with arc commands
            arc_radius = self.arrow_size * 0.3  # Smaller radius for a subtle curve
            
            # First arc from arrow tip to first point
            svg_parts.append(f'<path d="M {end_x} {svg_end_y} '
                           f'Q {end_x - self.arrow_size * 0.7 * np.cos(angle - arrow_angle/2)} '
                           f'{diagram_height - (end_y - self.arrow_size * 0.7 * np.sin(angle - arrow_angle/2))} '
                           f'{arrow1_x} {svg_arrow1_y}" '
                           f'stroke="{self.color}" stroke-width="{self.thickness}" '
                           f'stroke-linecap="round" fill="none"/>')
            
            # Second arc from arrow tip to second point  
            svg_parts.append(f'<path d="M {end_x} {svg_end_y} '
                           f'Q {end_x - self.arrow_size * 0.7 * np.cos(angle + arrow_angle/2)} '
                           f'{diagram_height - (end_y - self.arrow_size * 0.7 * np.sin(angle + arrow_angle/2))} '
                           f'{arrow2_x} {svg_arrow2_y}" '
                           f'stroke="{self.color}" stroke-width="{self.thickness}" '
                           f'stroke-linecap="round" fill="none"/>')
        
        return '\n'.join(svg_parts)

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