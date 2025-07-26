"""
Figure class - Main container for diagrams with title, size, and SVG output
"""

class Figure:
    def __init__(self):
        self._width = 800
        self._height = 600
        self._diagrams = []
    
    def size(self, dimensions):
        """Set figure size as [width, height]"""
        self._width, self._height = dimensions
        return self
    
    def addDiagram(self, diagram):
        """Add a diagram to the figure"""
        # Set the figure reference for bottom-relative positioning
        diagram.figure = self
        self._diagrams.append(diagram)
        return self
    
    def to_svg(self):
        """Generate SVG representation of the figure"""
        svg_parts = []
        
        # SVG header
        svg_parts.append(f'<svg width="{self._width}" height="{self._height}" xmlns="http://www.w3.org/2000/svg">')
        
        # Background
        svg_parts.append(f'<rect width="{self._width}" height="{self._height}" fill="white"/>')
        
        # Render all diagrams
        for diagram in self._diagrams:
            svg_parts.append(diagram.to_svg())
        
        svg_parts.append('</svg>')
        
        return '\n'.join(svg_parts)
    
    def save(self, filename):
        """Save figure as SVG file"""
        with open(filename, 'w') as f:
            f.write(self.to_svg()) 