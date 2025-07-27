"""
Spline class - Cubic-Hermite spline implementation
"""
import math

class Spline:
    """
    Cubic-Hermite spline (1 or more spans)

        points   – [(x, y), …]     anchor points *relative* to the axes origin
        tangents – [(dx, dy), …]   gradient vectors, same length as points
    """

    def __init__(self, points, tangents,
                 color="black", thickness=1, line_style="solid"):
        if len(points) < 2:
            raise ValueError("Need at least two points for a spline.")
        if len(points) != len(tangents):
            raise ValueError("points and tangents must be the same length.")

        self.points   = [list(p) for p in points]
        self.tangents = [list(v) for v in tangents]

        self.color       = color
        self.thickness   = thickness
        self.line_style  = line_style   # 'solid' | 'dashed'

    # ─────────────────────────────────────────────────────────── public helpers
    def style(self, line_style):
        if line_style not in ("solid", "dashed"):
            raise ValueError("line_style must be 'solid' or 'dashed'")
        self.line_style = line_style
        return self

    def set_color(self, c):   self.color     = c; return self
    def set_thickness(self, t): self.thickness = t; return self

    # ───────────────────────────────────────────────────────── internal utility
    @staticmethod
    def _to_svg_xy(pt, diag_h):
        """Flip y-axis for SVG coordinates."""
        return pt[0], diag_h - pt[1]

    # ─────────────────────────────────────────────────────────────── SVG export
    def to_svg(self, diagram_w, diagram_h):
        """
        Return a single SVG `<path>` element for all spans.
        Points **must already be absolute** when this is called
        (Axes.add_spline below takes care of that).
        """
        P  = self.points          # absolute anchors
        m  = self.tangents        # corresponding gradients

        # SVG path commands ---------------------------------------------------
        x0, y0 = self._to_svg_xy(P[0], diagram_h)
        cmds   = [f"M {x0} {y0}"]

        for i in range(len(P) - 1):
            P0, P1   = P[i],   P[i + 1]
            m0, m1   = m[i],   m[i + 1]

            # Characteristic span length (for sensible tangent scale)
            h = math.hypot(P1[0] - P0[0], P1[1] - P0[1]) or 1.0

            # Bézier control points from Hermite data
            C1 = (P0[0] + m0[0] * h / 3.0, P0[1] + m0[1] * h / 3.0)
            C2 = (P1[0] - m1[0] * h / 3.0, P1[1] - m1[1] * h / 3.0)

            c1x, c1y = self._to_svg_xy(C1, diagram_h)
            c2x, c2y = self._to_svg_xy(C2, diagram_h)
            p1x, p1y = self._to_svg_xy(P1, diagram_h)

            cmds.append(f"C {c1x} {c1y} {c2x} {c2y} {p1x} {p1y}")

        dash = "none" if self.line_style == "solid" else "5,3"

        d_attr = " ".join(cmds)
        return (f'<path d="{d_attr}" stroke="{self.color}" '
                f'stroke-width="{self.thickness}" stroke-dasharray="{dash}" '
                f'stroke-linecap="round" fill="none"/>') 