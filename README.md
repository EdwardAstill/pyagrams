# PyAgrams

**Simple Python diagramming library for creating beautiful SVG diagrams with clean, readable code.**

PyAgrams provides an intuitive API for creating technical diagrams, mathematical visualizations, and scientific illustrations. Built with a modern, extensible architecture that scales from simple 2D plots to complex multi-diagram figures.

## ✨ Features

- **Clean API**: Intuitive, chainable methods for rapid diagram creation
- **Flexible Styling**: Unified style system with themes and customizable appearance
- **Modular Architecture**: Extensible design ready for 2D and 3D geometry
- **Multiple Exports**: SVG output with PDF and other formats planned
- **Vector Graphics**: Resolution-independent output perfect for publications
- **Zero Dependencies**: Pure Python with only NumPy for vector math

## 🚀 Quick Start

```python
import pyagrams as pa

# Create a figure
fig = pa.figure.size([400, 300])

# Create a diagram
diagram = pa.diagram().size(300, 200).position(50, 50)

# Add coordinate axes
axes = pa.axes([20, 20], [120, 80])

# Add geometric objects
pa.point(5, [10, 10]).add_to(axes)                    # Point at (10, 10)
pa.vector([0, 0], [30, 40], color="red").add_to(axes) # Red vector
pa.spline([[0,0],[40,20]], [[1,0],[0,-1]], color="blue").add_to(axes)  # Blue curve

# Assemble and save
diagram.add_axes(axes)
fig.addDiagram(diagram)
fig.save("my_diagram.svg")
```

## 📚 Core Concepts

### Architecture Overview

PyAgrams uses a hierarchical structure:

```
Figure (canvas)
  └── Diagram (container)
      └── Axes (coordinate system)
          └── Geometry Objects (points, vectors, splines)
```

### Key Components

- **Figure**: Top-level canvas that contains multiple diagrams
- **Diagram**: Container for organizing related content with positioning
- **Axes**: Coordinate system providing origin and scale reference
- **Geometry Objects**: Drawable primitives (points, vectors, splines)

## 🎨 Styling System

PyAgrams uses a unified styling approach:

```python
from pyagrams.core import Style, Theme

# Custom styles
red_style = Style(color="red", thickness=2.5, line_style="solid")
vector = pa.vector([0, 0], [10, 10], style=red_style)

# Or use keyword arguments
vector = pa.vector([0, 0], [10, 10], color="red", thickness=2.5)

# Built-in themes
axes = pa.axes([0, 0], [100, 100])
axes.style = Theme.highlight  # Pre-defined theme
```

## 📐 Geometry Objects

### Points
```python
# Basic point
point = pa.point(size=3, coords=[10, 20])

# Styled point
point = pa.point(5, [15, 25], color="blue")
```

### Vectors
```python
# Basic vector (dashed by default)
vector = pa.vector(position=[0, 0], direction=[10, 15])

# Solid vector with custom appearance
vector = pa.vector([5, 5], [20, 10], color="green", line_style="solid", thickness=2)
```

### Splines (Curves)
```python
# Cubic Hermite spline
points = [[0, 0], [20, 10], [40, 5]]
tangents = [[1, 0], [0, 1], [-1, 0]]  # Tangent vectors at each point
spline = pa.spline(points, tangents, color="purple", thickness=1.5)
```

## 🏗️ Advanced Usage

### Multiple Diagrams
```python
fig = pa.figure.size([800, 600])

# First diagram
diagram1 = pa.diagram().size(350, 250).position(50, 100)
axes1 = pa.axes([25, 25], [100, 60])
pa.point(3, [50, 30]).add_to(axes1)
diagram1.add_axes(axes1)

# Second diagram  
diagram2 = pa.diagram().size(300, 200).position(450, 150)
axes2 = pa.axes([20, 20], [80, 50])
pa.vector([0, 0], [60, 40], color="red").add_to(axes2)
diagram2.add_axes(axes2)

# Add both to figure
fig.addDiagram(diagram1)
fig.addDiagram(diagram2)
fig.save("multi_diagram.svg")
```

### Coordinate Systems and Ticks
```python
axes = pa.axes([10, 10], [200, 150])

# Add tick marks
axes.add_ticks(
    spacing=25,          # Every 25 units
    length=8,            # 8 pixel tick length
    orientation="both",  # x and y axes
    placement="inside"   # Inside the axes
)

# Style the axes
axes.style("solid")  # Make axes solid instead of dashed
```

### Advanced Styling
```python
from pyagrams.core import Style, Theme

# Create custom style
my_style = Style(
    color="#FF6B35",      # Orange color
    thickness=3.0,        # Thick lines
    line_style="dashed"   # Dashed style
)

# Apply to objects
vector = pa.vector([0, 0], [50, 30], style=my_style)

# Use predefined themes
axes.style = Theme.subtle    # Light gray, thin lines
vector.style = Theme.highlight  # Red, thick, solid
```

## 🏛️ Package Architecture

PyAgrams is organized into clean, focused modules:

```
pyagrams/
├── core/
│   ├── style.py          # Style & Theme classes
│   ├── primitives.py     # BaseDrawable & base classes
│   ├── geometry2d.py     # 2D points, vectors, splines
│   └── geometry3d.py     # 3D geometry (future)
├── scene/
│   ├── axes.py           # Coordinate system management
│   └── diagram.py        # Container and layout
├── exporters/
│   └── svg.py            # SVG output (PDF planned)
├── figure.py             # Top-level canvas
└── __init__.py           # Public API
```

### Design Principles

- **Separation of Concerns**: Each module has a focused responsibility
- **Extensibility**: Easy to add new geometry types and export formats
- **Style Consistency**: Unified styling system across all objects
- **Future-Ready**: Architecture supports 3D expansion

## 🔧 API Reference

### Public API Functions

```python
import pyagrams as pa

# Singletons for convenience
pa.figure          # Main figure instance
pa.diagram()       # Create new diagram
pa.axes()          # Create new axes
pa.point()         # Create new point
pa.vector()        # Create new vector  
pa.spline()        # Create new spline
```

### Method Chaining

Most PyAgrams methods return `self`, enabling clean chaining:

```python
diagram = (pa.diagram()
           .size(300, 200)
           .position(50, 50)
           .fill("lightblue"))

axes = (pa.axes([20, 20], [120, 80])
        .style("solid")
        .add_ticks(25, orientation="both"))
```

### Export Options

```python
# SVG (current)
fig.save("diagram.svg")

# With backend specification (future)
fig.save("diagram.pdf", backend="pdf")  # Planned
fig.save("diagram.png", backend="raster")  # Planned
```

## 🔮 Future Development

### Planned Features

- **3D Geometry**: Points, vectors, and surfaces in 3D space
- **Additional Exports**: PDF, PNG, and LaTeX/TikZ output
- **Enhanced Primitives**: Text, circles, polygons, and mathematical symbols
- **Animation**: Time-based diagrams and interactive SVG
- **Themes**: Extended theme system with scientific/engineering presets

### 3D Expansion (Coming Soon)

```python
# Future 3D API preview
from pyagrams.core.geometry3d import Point3D, Vector3D, Axes3D

axes3d = Axes3D([0, 0, 0], size=[100, 100, 100])
point3d = Point3D(x=10, y=20, z=15)
vector3d = Vector3D([0, 0, 0], [10, 10, 10])
```

## 📖 Examples

Check out the included examples:

- `example.py` - Basic multi-diagram figure
- `vector_demo.py` - Vector styling demonstration

## 🤝 Contributing

PyAgrams is designed for extensibility. Common contribution areas:

- **New Geometry Types**: Add to `core/geometry2d.py` or `core/geometry3d.py`
- **Export Formats**: Create new exporters in `exporters/`
- **Styling Enhancements**: Extend the `Style` and `Theme` system
- **Documentation**: Examples and tutorials

## 📄 License

MIT License - see LICENSE file for details.

---

**PyAgrams** - Making technical diagrams as simple as they should be.
