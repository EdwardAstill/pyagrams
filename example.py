#!/usr/bin/env python3
"""
Example script demonstrating the simplified pyagrams API
"""

import sys
from pathlib import Path

# Add src to path so we can import pyagrams
sys.path.insert(0, str(Path(__file__).parent / "src"))

import pyagrams

# Create figure and set properties
figure = pyagrams.figure
figure.title("title", [400, 30])  # coords control the position of the title
figure.size([800, 600])

# Create first diagram (automatically added as first)
diagram1 = pyagrams.diagram()
diagram1.size(300, 200).position(50, 100)
# Add some elements to diagram1 to make it visible
axes1 = diagram1.addAxes([50, 150])  # axes in bottom-left of diagram1
axes1.addPoint(1, [20, 30])  # add a point
axes1.addLine([0, 0], [40, 20])  # add a line

figure.addDiagram(diagram1)

# Create second diagram  
diagram2 = pyagrams.diagram()
diagram2.size(250, 180).position(400, 120)
axes = diagram2.addAxes([50, 130])  # puts a set of axis in bottom left corner of diagram
size = 1
axes.addPoint(size, [30, 40])  # coordinates [d, c] from your example

figure.addDiagram(diagram2)  # because diagram2 was added after it is overlaying number 1

# Generate and save the SVG
figure.save("example_output.svg")
print("Example diagram saved as: example_output.svg")
print("Open in browser to view the result!") 