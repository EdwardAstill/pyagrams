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
        
        # Label functionality
        self.label = None
        self.label_position = "auto"  # "auto", "above", "below", "left", "right", or custom [x, y]
    
    def set_label(self, text, position="auto"):
        """Set label text and position"""
        self.label = text
        self.label_position = position
        return self
    
    def _get_label_position(self, object_bbox):
        """Calculate label position based on object bounding box and label_position setting"""
        # Calculate center of the object
        center_x = (object_bbox.min_x + object_bbox.max_x) / 2
        center_y = (object_bbox.min_y + object_bbox.max_y) / 2
        
        if self.label_position == "auto":
            # Default behavior - for vectors, place below center
            return [center_x, object_bbox.min_y - 10]  # 10 pixels below
        elif self.label_position == "above":
            return [center_x, object_bbox.max_y + 5]  # 5 pixels above
        elif self.label_position == "below":
            return [center_x, object_bbox.min_y - 10]
        elif self.label_position == "left":
            return [object_bbox.min_x - 10, center_y]
        elif self.label_position == "right":
            return [object_bbox.max_x + 5, center_y]  # 5 pixels to the right
        elif isinstance(self.label_position, (list, tuple)) and len(self.label_position) == 2:
            # Check if it's a position vector (relative to center) or absolute coordinates
            # If the values are small (likely relative offsets), treat as position vector
            dx, dy = self.label_position
            if abs(dx) <= 50 and abs(dy) <= 50:  # Likely a position vector
                return [center_x + dx, center_y + dy]
            else:  # Likely absolute coordinates
                return list(self.label_position)
        else:
            # Fallback to auto
            return [center_x, object_bbox.min_y - 10]
    
    def _generate_label_svg(self, label_pos, diagram_height):
        """Generate SVG for the label"""
        if not self.label:
            return ""
        
        # Convert to SVG coordinates
        svg_x = label_pos[0]
        svg_y = diagram_height - label_pos[1]
        
        return f'<text x="{svg_x}" y="{svg_y}" text-anchor="middle" dominant-baseline="middle" ' \
               f'font-family="Times New Roman, Georgia, serif" font-size="8" fill="{self.style.color}">{self.label}</text>'
    
    @abstractmethod
    def to_svg(self, diagram_width: float, diagram_height: float) -> str:
        """Generate SVG representation of the object"""
        pass
    
    def bbox(self) -> BoundingBox:
        """Return bounding box (optional for now)"""
        # Default implementation - can be overridden by subclasses
        return BoundingBox(0, 0, 0, 0) 