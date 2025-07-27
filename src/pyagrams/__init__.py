"""
PyAgrams - Simple Python diagramming library
"""

from .figure import Figure
from .scene.diagram import Diagram
from .scene.axes import Axes
from .core.geometry2d import Point, Vector, Spline

# Create module-level instances for convenient access
figure = Figure()
diagram = Diagram
axes = Axes
point = Point
vector = Vector
spline = Spline

__all__ = ['Figure', 'Diagram', 'figure', 'diagram', 'Axes', 'Point', 'Vector', 'Spline', 'axes', 'point', 'vector', 'spline'] 