#!/usr/bin/env python3
"""
Demo script showing the new Vector class functionality
"""

import sys
from pathlib import Path

# Add src to path so we can import pyagrams
sys.path.insert(0, str(Path(__file__).parent / "src"))

from pyagrams.diagram import Vector, Axes, Diagram
from pyagrams.figure import Figure

def main():
    """Demonstrate Vector class usage"""
    print("Creating Vector demonstration...")
    
    # Create figure
    figure = Figure()
    figure.size([600, 400])
    
    # Create diagram
    diagram = Diagram(width=500, height=300, x=50, y=50, figure=figure)
    
    # Create axes using Vector class (default dashed style)
    axes = Axes([50, 50], [150, 100])
    axes.add_point(2, [75, 75])  # Add a point
    diagram.add_axes(axes)
    
    # Change axes style to solid for comparison
    axes2 = Axes([250, 50], [120, 80])
    axes2.style("solid")  # Solid style vectors
    axes2.add_point(3, [90, 60])
    diagram.add_axes(axes2)
    
    # Add diagram to figure
    figure.add_diagram(diagram)
    
    # Save the result
    figure.save("vector_demo.svg")
    print("Vector demo saved as: vector_demo.svg")
    print("You can see:")
    print("- Left axes: dashed vectors with arrow tips (default)")
    print("- Right axes: solid vectors with arrow tips")
    print("- Both have points to show coordinate system works")

if __name__ == "__main__":
    main() 