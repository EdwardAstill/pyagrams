"""
Vector class - A line with arrow tip defined by position and direction vectors
"""
import numpy as np

class Vector:
    """
    Vector class - A line with arrow tip defined by position and direction vectors
    """
    def __init__(self, position=None, direction=None):
        self.position = position or [0, 0]  # Starting point of the vector
        self.direction = direction or [10, 10]  # Direction and magnitude
        self.color = "black"
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