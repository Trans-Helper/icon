import math
from pathlib import Path

import cairosvg
import svg

OUT = Path("output")


def main():
    a = 1024
    cx = cy = a / 2
    outer_r = (a - 60) / 2

    dark = "#1a1a2e"

    elements = [
        svg.Rect(x=0, y=0, width=a, height=a, fill="white"),
    ]

    # Outer bezel
    elements.append(
        svg.Circle(cx=cx, cy=cy, r=outer_r, fill="none", stroke=dark, stroke_width=12)
    )
    # Inner ring
    elements.append(
        svg.Circle(
            cx=cx, cy=cy, r=outer_r - 42, fill="none", stroke=dark, stroke_width=2
        )
    )
    # Decorative dashed ring
    elements.append(
        svg.Circle(
            cx=cx,
            cy=cy,
            r=outer_r - 62,
            fill="none",
            stroke=dark,
            stroke_width=1,
            stroke_dasharray=[3, 6],
        )
    )
    # Inner compass ring
    elements.append(
        svg.Circle(
            cx=cx, cy=cy, r=140, fill="none", stroke=dark, stroke_width=1, opacity=0.25
        )
    )
    # Capital H at center (behind the pointer), drawn with rounded rects
    hw, hh = 40, 340
    gap = 160
    for x in [cx - hw - gap // 2, cx + gap // 2]:
        elements.append(
            svg.Rect(
                x=x,
                y=cy - hh // 2,
                width=hw,
                height=hh,
                rx=5,
                ry=5,
                fill=dark,
            )
        )
    elements.append(
        svg.Rect(
            x=cx - (hw + gap) // 2,
            y=cy - hw // 2,
            width=hw + gap,
            height=hw,
            rx=5,
            ry=5,
            fill=dark,
        )
    )

    # 45-degree compass needle (two triangles)
    needle_angle = 45
    trig_a = math.radians(270 + needle_angle)
    ptr_len = outer_r - 120
    ptr_width = 90
    half_w = ptr_width / 2

    dx = math.cos(trig_a)
    dy = math.sin(trig_a)
    px = math.cos(trig_a + math.pi / 2)
    py = math.sin(trig_a + math.pi / 2)

    elements.append(
        svg.Polygon(
            points=[
                (cx + ptr_len * dx, cy + ptr_len * dy),
                (cx + half_w * px, cy + half_w * py),
                (cx - half_w * px, cy - half_w * py),
            ],
            fill="#f5abb9",
        )
    )
    elements.append(
        svg.Polygon(
            points=[
                (cx - ptr_len * dx, cy - ptr_len * dy),
                (cx - half_w * px, cy - half_w * py),
                (cx + half_w * px, cy + half_w * py),
            ],
            fill="#5bcffa",
        )
    )

    # Center outer circle
    elements.append(svg.Circle(cx=cx, cy=cy, r=34, fill="white", stroke="none"))
    # Center inner dot
    # elements.append(svg.Circle(cx=cx, cy=cy, r=5, fill="white", stroke="none"))
    # Tick marks (216 ticks, every 5/3 degrees)
    tick_top = cy - outer_r + 16
    total_ticks = 216

    for i in range(total_ticks):
        angle = i * 5 / 3
        mod = i % 54

        if mod == 0:
            w, h, rad, fill, op = 10, 40, 5, dark, 1.0
        elif mod % 18 == 0:
            w, h, rad, fill, op = 7, 28, 3.5, dark, 1.0
        elif mod % 3 == 0:
            w, h, rad, fill, op = 3, 14, 1.5, dark, 0.35
        else:
            w, h, rad, fill, op = 2, 9, 1, dark, 0.2

        elements.append(
            svg.G(
                transform=[svg.Rotate(angle, cx, cy)],
                elements=[
                    svg.Rect(
                        x=cx - w / 2,
                        y=tick_top,
                        width=w,
                        height=h,
                        rx=rad,
                        ry=rad,
                        fill=fill,
                        opacity=op,
                    )
                ],
            )
        )

    # Cardinal diamonds (extending slightly outside bezel)
    diamond_y = cy - outer_r - 2
    for angle in [0, 90, 180, 270]:
        elements.append(
            svg.G(
                transform=[svg.Rotate(angle, cx, cy)],
                elements=[
                    svg.Rect(
                        x=cx - 13,
                        y=diamond_y - 13,
                        width=26,
                        height=26,
                        rx=5,
                        ry=5,
                        fill=dark,
                        transform=[svg.Rotate(45, cx, diamond_y)],
                    )
                ],
            )
        )

    OUT.mkdir(parents=True, exist_ok=True)

    svg_str = str(svg.SVG(width=a, height=a, elements=elements))
    (OUT / "output.svg").write_text(svg_str)
    print("SVG generated: output/output.svg")

    sizes = [16, 32, 48, 64, 96, 128, 256, 512]
    for s in sizes:
        cairosvg.svg2png(
            bytestring=svg_str.encode(),
            output_width=s,
            output_height=s,
            write_to=str(OUT / f"icon-{s}.png"),
        )
    names = [f"icon-{s}.png" for s in sizes]
    print(f"PNGs exported to output/: {', '.join(names)}")


if __name__ == "__main__":
    main()
