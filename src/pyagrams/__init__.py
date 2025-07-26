"""
PyAgrams - Simple Python diagramming library
"""

from .figure import Figure
from .diagram import Diagram, Axes, Point, Vector

# Create module-level instances for convenient access
figure = Figure()
diagram = Diagram
axes = Axes
point = Point
vector = Vector

__all__ = ['Figure', 'Diagram', 'figure', 'diagram', 'Axes', 'Point', 'Vector', 'axes', 'point', 'vector'] 