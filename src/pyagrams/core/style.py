"""
Style and Theme classes for managing visual attributes
"""
from dataclasses import dataclass


@dataclass
class Style:
    """Style attributes for drawable objects"""
    color: str = "black"
    thickness: float = 2.0
    line_style: str = "solid"  # 'solid' | 'dashed'

    @property
    def dasharray(self):
        """Convert line_style to SVG stroke-dasharray string"""
        return "none" if self.line_style == "solid" else "5,3"


class Theme:
    """Collection of default styles for different object types"""
    
    default = Style()
    axes = Style(color="gray", thickness=1.0, line_style="dashed")
    highlight = Style(color="red", thickness=2.5, line_style="solid")
    subtle = Style(color="lightgray", thickness=1.0, line_style="dashed") 