"""
2D Geometry classes and primitives for PyAgrams
"""
import math
import numpy as np
from typing import List, Tuple
from .primitives import BaseDrawable, BoundingBox


# ============================================================================
# Basic 2D Geometry Utilities
# ============================================================================

class Point2D:
    """Basic 2D point representation"""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def to_list(self) -> List[float]:
        return [self.x, self.y]
    
    def __add__(self, other):
        return Point2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Point2D(self.x - other.x, self.y - other.y)


class Vector2D:
    """Basic 2D vector representation"""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def to_list(self) -> List[float]:
        return [self.x, self.y]
    
    def magnitude(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5


class Transform:
    """Simple 2D transformation (translation for now)"""
    def __init__(self, dx: float = 0, dy: float = 0):
        self.dx = dx
        self.dy = dy
    
    def apply_to_point(self, point: List[float]) -> List[float]:
        return [point[0] + self.dx, point[1] + self.dy]


# ============================================================================
# Drawable 2D Geometry Primitives
# ============================================================================

class Point(BaseDrawable):
    """
    Point class - Container for a point with x, y, size, and style
    Add a point to axes by doing axes.add_point(Point(x, y, size))
    or Point(x, y, size).add_to(axes)
    """
    def __init__(self, size, coords, **style_kw):
        super().__init__(**style_kw)
        self.coords = coords
        self.size = size
        
        # Labels are empty by default
    
    def bbox(self) -> BoundingBox:
        """Calculate bounding box for the point"""
        x, y = self.coords
        radius = self.size / 2
        return BoundingBox(x - radius, y - radius, x + radius, y + radius)
    
    def add_to(self, axes):
        """Add the point to the axes"""
        axes.add_point(self.size, self.coords)
        return self
    
    def to_svg(self, diagram_width: float, diagram_height: float) -> str:
        """Generate SVG representation of the point"""
        svg_parts = []
        
        # Convert coordinates to SVG space
        svg_y = diagram_height - self.coords[1]
        svg_x = self.coords[0]
        
        # Draw the point
        svg_parts.append(f'<circle cx="{svg_x}" cy="{svg_y}" r="{self.size/2}" fill="{self.style.color}"/>')
        
        # Add label if present
        if self.label:
            bbox = self.bbox()
            label_pos = self._get_label_position(bbox)
            svg_parts.append(self._generate_label_svg(label_pos, diagram_height))
        
        return '\n'.join(svg_parts)


class Vector(BaseDrawable):
    """
    Vector class - A line with arrow tip defined by position and direction vectors
    """
    def __init__(self, position=None, direction=None, **style_kw):
        # Set default style for vectors (dashed)
        if 'line_style' not in style_kw:
            style_kw['line_style'] = 'dashed'
        if 'thickness' not in style_kw:
            style_kw['thickness'] = 1
        
        super().__init__(**style_kw)
        self.position = position or [0, 0]  # Starting point of the vector
        self.direction = direction or [10, 10]  # Direction and magnitude
        self.arrow_size = 8  # Size of arrow tip (increased from 5)
        
        # Labels are empty by default
        
    def bbox(self) -> BoundingBox:
        """Calculate bounding box for the vector including arrow tip"""
        start_x, start_y = self.position
        end_x = start_x + self.direction[0]
        end_y = start_y + self.direction[1]
        
        # Calculate arrow tip points for bounding box
        if self.direction[0] != 0 or self.direction[1] != 0:
            angle = np.arctan2(self.direction[1], self.direction[0])
            arrow_angle = np.pi / 9  # 20 degrees
            
            arrow1_x = end_x - self.arrow_size * np.cos(angle - arrow_angle)
            arrow1_y = end_y - self.arrow_size * np.sin(angle - arrow_angle)
            
            arrow2_x = end_x - self.arrow_size * np.cos(angle + arrow_angle)
            arrow2_y = end_y - self.arrow_size * np.sin(angle + arrow_angle)
            
            min_x = min(start_x, end_x, arrow1_x, arrow2_x)
            max_x = max(start_x, end_x, arrow1_x, arrow2_x)
            min_y = min(start_y, end_y, arrow1_y, arrow2_y)
            max_y = max(start_y, end_y, arrow1_y, arrow2_y)
        else:
            min_x = max_x = start_x
            min_y = max_y = start_y
        
        return BoundingBox(min_x, min_y, max_x, max_y)
        
    def style(self, line_style):
        """Set vector line style: 'dashed' or 'solid'"""
        if line_style not in ("dashed", "solid"):
            raise ValueError("line_style must be 'dashed' or 'solid'")
        self.style.line_style = line_style
        return self
        
    def color(self, color):
        """Set vector color"""
        self.style.color = color
        return self
        
    def thickness(self, thickness):
        """Set vector thickness"""
        self.style.thickness = thickness
        return self
    
    def add_to(self, axes):
        """Add the vector to the axes"""
        # Convert absolute position to relative position for axes
        relative_position = [
            self.position[0] - axes.position[0],
            self.position[1] - axes.position[1] 
        ]
        axes.add_vector(relative_position, self.direction)
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
        
        # Use style for line appearance
        dash_length = 8
        dash_gap = 2
        dash_array = f"{dash_length},{dash_gap}" if self.style.line_style == "dashed" else "none"
        
        # Draw main line
        svg_parts.append(f'<line x1="{start_x}" y1="{svg_start_y}" x2="{end_x}" y2="{svg_end_y}" '
                        f'stroke="{self.style.color}" stroke-width="{self.style.thickness}" stroke-dasharray="{dash_array}" '
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
            if self.style.line_style == "dashed":
                # Gap fill line should be exactly the length of the dash gap
                gap_fill_length = dash_gap
                gap_fill_end_x = end_x - gap_fill_length * np.cos(angle)
                gap_fill_end_y = end_y - gap_fill_length * np.sin(angle)
                svg_gap_fill_end_y = diagram_height - gap_fill_end_y
                
                svg_parts.append(f'<line x1="{end_x}" y1="{svg_end_y}" x2="{gap_fill_end_x}" y2="{svg_gap_fill_end_y}" '
                               f'stroke="{self.style.color}" stroke-width="{self.style.thickness}"/>')
            
            # Draw arrow tip as curved arcs with round linecaps
            # Create a curved arrow tip using SVG path with arc commands
            arc_radius = self.arrow_size * 0.3
            
            # First arc from arrow tip to first point
            svg_parts.append(f'<path d="M {end_x} {svg_end_y} '
                           f'Q {end_x - self.arrow_size * 0.7 * np.cos(angle - arrow_angle/2)} '
                           f'{diagram_height - (end_y - self.arrow_size * 0.7 * np.sin(angle - arrow_angle/2))} '
                           f'{arrow1_x} {svg_arrow1_y}" '
                           f'stroke="{self.style.color}" stroke-width="{self.style.thickness}" '
                           f'stroke-linecap="round" fill="none"/>')
            
            # Second arc from arrow tip to second point  
            svg_parts.append(f'<path d="M {end_x} {svg_end_y} '
                           f'Q {end_x - self.arrow_size * 0.7 * np.cos(angle + arrow_angle/2)} '
                           f'{diagram_height - (end_y - self.arrow_size * 0.7 * np.sin(angle + arrow_angle/2))} '
                           f'{arrow2_x} {svg_arrow2_y}" '
                           f'stroke="{self.style.color}" stroke-width="{self.style.thickness}" '
                           f'stroke-linecap="round" fill="none"/>')
        
        # Add label if present
        if self.label:
            bbox = self.bbox()
            label_pos = self._get_label_position(bbox)
            svg_parts.append(self._generate_label_svg(label_pos, diagram_height))
        
        return '\n'.join(svg_parts)


class Spline(BaseDrawable):
    """
    Cubic-Hermite spline (1 or more spans)

        points   – [(x, y), …]     anchor points *relative* to the axes origin
        tangents – [(dx, dy), …]   gradient vectors, same length as points
    """

    def __init__(self, points, tangents, **style_kw):
        if len(points) < 2:
            raise ValueError("Need at least two points for a spline.")
        if len(points) != len(tangents):
            raise ValueError("points and tangents must be the same length.")

        # Set default style for splines
        if 'thickness' not in style_kw:
            style_kw['thickness'] = 1
        
        super().__init__(**style_kw)
        self.points   = [list(p) for p in points]
        self.tangents = [list(v) for v in tangents]
        
        # Labels are empty by default

    def bbox(self) -> BoundingBox:
        """Calculate bounding box for the spline"""
        if not self.points:
            return BoundingBox(0, 0, 0, 0)
        
        x_coords = [p[0] for p in self.points]
        y_coords = [p[1] for p in self.points]
        
        return BoundingBox(
            min(x_coords), min(y_coords),
            max(x_coords), max(y_coords)
        )

    # ─────────────────────────────────────────────────────────── public helpers
    def style(self, line_style):
        """Set spline line style: 'solid' or 'dashed'"""
        if line_style not in ("solid", "dashed"):
            raise ValueError("line_style must be 'solid' or 'dashed'")
        self.style.line_style = line_style
        return self

    def set_color(self, c):
        """Set spline color"""
        self.style.color = c
        return self
        
    def set_thickness(self, t):
        """Set spline thickness"""
        self.style.thickness = t
        return self

    def add_to(self, axes):
        """Add the spline to the axes"""
        axes.add_spline(self)
        return self

    # ───────────────────────────────────────────────────────── internal utility
    @staticmethod
    def _to_svg_xy(pt, diag_h):
        """Flip y-axis for SVG coordinates."""
        return pt[0], diag_h - pt[1]

    # ─────────────────────────────────────────────────────────────── SVG export
    def to_svg(self, diagram_w, diagram_h):
        """
        Return a single SVG `<path>` element for all spans.
        Points **must already be absolute** when this is called
        (Axes.add_spline below takes care of that).
        """
        svg_parts = []
        
        P  = self.points          # absolute anchors
        m  = self.tangents        # corresponding gradients

        # SVG path commands ---------------------------------------------------
        x0, y0 = self._to_svg_xy(P[0], diagram_h)
        cmds   = [f"M {x0} {y0}"]

        for i in range(len(P) - 1):
            P0, P1   = P[i],   P[i + 1]
            m0, m1   = m[i],   m[i + 1]

            # Characteristic span length (for sensible tangent scale)
            h = math.hypot(P1[0] - P0[0], P1[1] - P0[1]) or 1.0

            # Bézier control points from Hermite data
            C1 = (P0[0] + m0[0] * h / 3.0, P0[1] + m0[1] * h / 3.0)
            C2 = (P1[0] - m1[0] * h / 3.0, P1[1] - m1[1] * h / 3.0)

            c1x, c1y = self._to_svg_xy(C1, diagram_h)
            c2x, c2y = self._to_svg_xy(C2, diagram_h)
            p1x, p1y = self._to_svg_xy(P1, diagram_h)

            cmds.append(f"C {c1x} {c1y} {c2x} {c2y} {p1x} {p1y}")

        # Use style for appearance
        d_attr = " ".join(cmds)
        svg_parts.append(f'<path d="{d_attr}" stroke="{self.style.color}" '
                f'stroke-width="{self.style.thickness}" stroke-dasharray="{self.style.dasharray}" '
                f'stroke-linecap="round" fill="none"/>')
        
        # Add label if present
        if self.label:
            bbox = self.bbox()
            label_pos = self._get_label_position(bbox)
            svg_parts.append(self._generate_label_svg(label_pos, diagram_h))
        
        return '\n'.join(svg_parts) 