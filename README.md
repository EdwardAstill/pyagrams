# PyAgrams

A simple Python diagramming library that generates SVG diagrams.

## How PyAgrams Draws Stuff

PyAgrams uses a hierarchical structure to draw diagrams:

### Architecture

1. **Figure** - The main container that holds everything
   - Sets the overall canvas size (width × height)
   - Contains an optional title
   - Holds multiple diagrams
   - Generates the final SVG output

2. **Diagram** - Individual diagram containers within a figure
   - Has its own size and position within the figure
   - Contains axes and geometric primitives
   - Each diagram is positioned using x,y coordinates relative to the figure

3. **Axes** - Coordinate systems within diagrams
   - Define the origin point within a diagram
   - Can be scaled up or down
   - Support configurable arrows (up, down, left, right)
   - Draw coordinate lines and arrows

4. **Primitives** - Basic geometric shapes
   - Points, lines, and other shapes (currently being expanded)
   - Positioned relative to the axes coordinate system

### Drawing Process

1. **SVG Generation**: Everything is converted to SVG markup
   - Figure creates the main SVG container with specified dimensions
   - Each diagram becomes a `<g>` (group) element with transform positioning
   - Axes render as `<line>` elements for coordinate lines and `<polygon>` elements for arrows
   - Primitives render as appropriate SVG elements

2. **Coordinate Systems**:
   - Figure coordinates: Top-left origin, used for positioning diagrams
   - Diagram coordinates: Top-left origin, used for positioning axes
   - Axis coordinates: Custom origin, used for positioning primitives

3. **Rendering Flow**:
   ```
   Figure.to_svg() → Diagram.to_svg() → Axis.to_svg() → Primitive.to_svg()
   ```

### Key Drawing Features

- **Scalable**: All elements scale proportionally
- **Positionable**: Diagrams can be placed anywhere within the figure
- **Configurable**: Axes can have different arrow configurations
- **SVG Output**: Generates clean, viewable SVG files
- **Chained API**: Methods return self for easy chaining

### Example Usage

```python
import pyagrams

# Create a figure
figure = pyagrams.figure
figure.title("My Diagram", [400, 30])
figure.size([800, 600])

# Create a diagram
diagram = pyagrams.diagram()
diagram.size(300, 200).position(50, 100)

# Add axes
axes = diagram.addAxes([50, 150])
axes.set_size(1.5)
axes.set_arrows(up=True, down=False, left=False, right=True)

# Add to figure and save
figure.addDiagram(diagram)
figure.save("output.svg")
```

The package draws by building up SVG markup from the bottom up, starting with primitives, then axes, then diagrams, and finally the complete figure.
