"""
Base classes for drawable objects
"""
from abc import ABC, abstractmethod
from .style import Style


class BoundingBox:
    """2D bounding box for spatial operations"""
    def __init__(self, min_x: float, min_y: float, max_x: float, max_y: float):
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
    
    @property
    def width(self) -> float:
        return self.max_x - self.min_x
    
    @property
    def height(self) -> float:
        return self.max_y - self.min_y


class BaseDrawable(ABC):
    """Base class for all drawable objects"""
    
    def __init__(self, style: Style = None, **style_kw):
        """Initialize with style object or style keyword arguments"""
        if style is not None and style_kw:
            raise ValueError("Cannot specify both style object and style keywords")
        
        if style is not None:
            self.style = style
        else:
            self.style = Style(**style_kw)
    
    @abstractmethod
    def to_svg(self, diagram_width: float, diagram_height: float) -> str:
        """Generate SVG representation of the object"""
        pass
    
    def bbox(self) -> BoundingBox:
        """Return bounding box (optional for now)"""
        # Default implementation - can be overridden by subclasses
        return BoundingBox(0, 0, 0, 0) 