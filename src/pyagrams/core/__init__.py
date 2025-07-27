"""
Core module for PyAgrams - Contains fundamental classes
"""
from .style import Style, Theme
from .geometry2d import Point2D, Vector2D, Transform, Point, Vector, Spline
from .primitives import BaseDrawable, BoundingBox

# geometry3d is imported separately when needed since it's currently empty

__all__ = [
    'Style', 'Theme', 
    'Point2D', 'Vector2D', 'Transform', 'BoundingBox', 
    'Point', 'Vector', 'Spline',
    'BaseDrawable'
] 