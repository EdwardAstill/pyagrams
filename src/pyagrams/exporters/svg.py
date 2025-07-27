"""
SVG export functionality for PyAgrams
"""


class SVGExporter:
    """Handles SVG generation and coordinate transformation"""
    
    def __init__(self):
        pass
    
    def export(self, figure, filepath):
        """Export figure to SVG file"""
        svg_content = self.figure_to_svg(figure)
        with open(filepath, 'w') as f:
            f.write(svg_content)
    
    def figure_to_svg(self, figure):
        """Convert Figure object to SVG string"""
        svg_parts = []
        
        # SVG header
        svg_parts.append(f'<svg width="{figure._width}" height="{figure._height}" xmlns="http://www.w3.org/2000/svg">')
        
        # Background
        svg_parts.append(f'<rect width="{figure._width}" height="{figure._height}" fill="white"/>')
        
        # Render all diagrams
        for diagram in figure._diagrams:
            svg_parts.append(self.diagram_to_svg(diagram, figure))
        
        svg_parts.append('</svg>')
        
        return '\n'.join(svg_parts)
    
    def diagram_to_svg(self, diagram, figure):
        """Convert Diagram object to SVG string with proper positioning"""
        svg_parts = []
        
        # Calculate y position from bottom if figure reference is available
        if figure:
            # y is distance from bottom, so convert to distance from top
            y_from_top = figure._height - diagram.height - diagram.y
        else:
            y_from_top = diagram.y
        
        # Create a group for this diagram
        svg_parts.append(f'<g transform="translate({diagram.x},{y_from_top})">')
        
        # Diagram outline (black border for visibility)
        fill_value = diagram._fill if diagram._fill_enabled else "none"
        svg_parts.append(f'<rect width="{diagram.width}" height="{diagram.height}" '
                       f'fill="{fill_value}" stroke="black" stroke-width="2"/>')
        
        # Render points
        for px, py, psize in diagram._points:
            # SVG y=0 is top, so invert y for correct placement within the diagram
            svg_y = diagram.height - py
            svg_x = px
            svg_parts.append(f'<circle cx="{svg_x}" cy="{svg_y}" r="{psize/2}" fill="black"/>')

        # Render vectors
        for vector in diagram._vectors:
            svg_parts.append(vector.to_svg(diagram.width, diagram.height))

        # Render axes
        for axes in diagram.axes:
            svg_parts.append(self.axes_to_svg(axes, diagram.width, diagram.height))
         
        svg_parts.append('</g>')
        
        return '\n'.join(svg_parts)
    
    def axes_to_svg(self, axes, diagram_width, diagram_height):
        """Convert Axes object to SVG string"""
        svg_parts = []
        
        # Update vector styles before rendering
        axes._update_vector_styles()
        
        # Render x and y vectors
        svg_parts.append(axes.x_vector.to_svg(diagram_width, diagram_height))
        svg_parts.append(axes.y_vector.to_svg(diagram_width, diagram_height))

        # Render all objects in order
        for obj in axes.objects:
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