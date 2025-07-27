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
    
    # Add point using the new object-based approach
    point = pyagrams.Point(1, [20, 80])
    axes.add_object(point)
    
    # Add vector with position vector for label placement
    vector = pyagrams.Vector([10, 10], [30, 60])
    vector.set_label("v", [0, -15])  # Position label 15 pixels below center
    axes.add_object(vector)
    
    # Add another vector with different position vector
    vector2 = pyagrams.Vector([80, 10], [20, 40])
    vector2.set_label("w", [15, 0])  # Position label 15 pixels to the right of center
    axes.add_object(vector2)
    
    # Add a third vector with diagonal offset
    vector3 = pyagrams.Vector([40, 80], [25, -30])
    vector3.set_label("u", [10, 10])  # Position label 10 pixels right and 10 pixels up from center
    axes.add_object(vector3)
    
    points = [[10,10],[50,20],[100,10]]
    vects = [[1,1],[1,-1],[-1,0]]
    curve = pyagrams.Spline(points, vects)
    curve.set_label("Curved Path", [-20, 0])  # Position label 20 pixels to the left of center
    axes.add_object(curve)
    
    #you should be able to axes.add_object(object) or you use axes.add_<object_name>(object_parameters)

    diagram1.add_axes(axes)



    figure.addDiagram(diagram1)
    # figure.addDiagram(diagram2)

    
    # Save the result
    figure.save("demo.svg")
    print("Demo diagram saved as: demo.svg")
    print("Open in browser to view the result!")

if __name__ == "__main__":
    main()







