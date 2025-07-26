#!/usr/bin/env python3
"""
Simple demonstration of PyAgrams usage - simplified approach.
"""

# import sys
# from pathlib import Path

# # Add src to path so we can import pyagrams
# sys.path.insert(0, str(Path(__file__).parent / "src"))

import pyagrams

def main():
    """Create and save a simple demonstration diagram using the simplified API."""
    print("Creating PyAgrams demonstration...")
    
    # Create figure and set properties
    figure = pyagrams.figure
    figure.size([500, 400])
    
    # Create first diagram
    diagram1 = pyagrams.diagram()
    diagram1.size(400, 300).position(50, 50)
    
    # Create axes with position and size
    axes = pyagrams.axes([50, 50], [100, 200])
    axes.add_point(1, [20, 80])  # Point at (20, 80) relative to axes origin
    # axes.add_ticks(10, length=8, color="black", placement="middle")
    
    # Add vector to axes with relative coordinates [0, 0] means starting at axes origin
    axes.add_vector([10, 10], [30, 60])  # Vector starting at (10, 10) relative to axes origin
    
    diagram1.add_axes(axes)



    figure.addDiagram(diagram1)
    # figure.addDiagram(diagram2)

    
    # Save the result
    figure.save("demo.svg")
    print("Demo diagram saved as: demo.svg")
    print("Open in browser to view the result!")

if __name__ == "__main__":
    main()







