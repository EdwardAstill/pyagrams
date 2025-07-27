"""
Figure class - Main container for diagrams with title, size, and SVG output
"""
from .exporters import SVGExporter


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
        """Generate SVG representation of the figure (legacy method)"""
        exporter = SVGExporter()
        return exporter.figure_to_svg(self)
    
    def save(self, filename, backend="svg"):
        """Save figure to file with specified backend"""
        if backend == "svg":
            exporter = SVGExporter()
            exporter.export(self, filename)
        else:
            raise ValueError(f"Unsupported backend: {backend}. Currently only 'svg' is supported.")
            
        # TODO: Add support for other backends like PDF in the future
    
    def title(self, title_text, position=None):
        """Add title to figure (compatibility method)"""
        # For now, just store the title - could be rendered later
        self._title = title_text
        self._title_position = position or [self._width // 2, 30]
        return self 