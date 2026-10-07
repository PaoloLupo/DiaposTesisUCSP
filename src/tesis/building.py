"""Dibujo de la planta del caso de estudio; los datos viven en ``tesis.data.planta``."""

from dataclasses import dataclass
from typing import Literal

from gaanim import Anchor, Color, Composition, Drawable, Scene, Text, stagger

from tesis.data.planta import (
    AXIS_X,
    AXIS_Y,
    DEPTH,
    FLOOR_AREA,
    STAIR,
    THICKNESS,
    WALLS,
    WIDTH,
    Wall,
    density,
    wall_area_sum,
)
from tesis.theme import BRICK, CONCRETE, INK_SOFT, MONO, MUTED, RULE, STEEL

# Las secciones importan los datos de la planta desde aquí junto con el dibujo.
__all__ = [
    "AXIS_X",
    "AXIS_Y",
    "DEPTH",
    "FLOOR_AREA",
    "STAIR",
    "THICKNESS",
    "WALLS",
    "WIDTH",
    "Plan",
    "Wall",
    "density",
    "draw_plan",
    "grow_walls",
    "wall_area_sum",
    "wall_segments",
]


@dataclass
class Plan:
    """Objetos dibujados de una planta; ``walls`` usa etiquetas de Pier."""

    slab: Drawable
    void: Drawable
    walls: dict[str, Drawable]
    grid: list[Drawable]
    bubbles: list[Drawable]
    labels: dict[str, Text]
    origin: tuple[float, float]
    scale: float
    thickness: float  # espesor dibujado de los muros, en unidades de escena

    def to_scene(self, x: float, y: float) -> tuple[float, float]:
        ox, oy = self.origin
        return ox + x * self.scale, oy + y * self.scale

    def wall_box(self, name: str) -> tuple[float, float, float, float]:
        """Caja (izquierda, abajo, derecha, arriba) del muro dibujado, desde los datos.

        Evita ``bounds()``, que tras un ``play`` compila la escena hasta el cursor.
        Vale mientras el muro no se haya movido ni escalado después de dibujarlo.
        """
        _, wall, ax, ay, bx, by = next(s for s in wall_segments() if s[0] == name)
        cx, cy = self.to_scene((ax + bx) / 2, (ay + by) / 2)
        length = (bx - ax + by - ay) * self.scale
        w, h = (length, self.thickness) if wall.direction == "X" else (self.thickness, length)
        return cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2

    def by_direction(self, direction: str) -> list[Drawable]:
        return [d for name, d in self.walls.items() if name.startswith(direction)]

    def instances(self, base: str) -> list[Drawable]:
        """Muro y su simétrico: ``X1`` → [X1, X1_2]."""
        return [d for name, d in self.walls.items() if name.split("_")[0] == base]

    @property
    def all_walls(self) -> list[Drawable]:
        return list(self.walls.values())


def grow_walls(
    walls: list[Drawable],
    *,
    total: float = 0.9,
    duration: float = 0.4,
    origin: Literal["center", "edges", "random"] | tuple[float, float] = "center",
) -> Composition:
    """Los muros crecen en orden de distancia a ``origin``, no en el orden de la lista.

    Con el origen al centro, la planta se levanta desde el núcleo hacia la fachada.
    """
    return stagger(
        *[w.animate.grow_from_center().duration(duration) for w in walls],
        total=total,
        origin=origin,
    )


def wall_segments() -> list[tuple[str, Wall, float, float, float, float]]:
    """(etiqueta, muro, x0, y0, x1, y1) para ambas mitades del edificio."""
    segments = []
    for wall in WALLS:
        mirrored = wall.count == 2
        for suffix, flip in [("", False), ("_2", True)] if mirrored else [("", False)]:
            if wall.direction == "X":
                x0, x1 = wall.start, wall.end
                y0 = y1 = wall.fixed
            else:
                x0 = x1 = wall.fixed
                y0, y1 = wall.start, wall.end
            if flip:
                x0, x1 = WIDTH - x1, WIDTH - x0
            segments.append((wall.name + suffix, wall, x0, y0, x1, y1))
    return segments


def draw_plan(
    scene: Scene,
    center: tuple[float, float],
    width: float,
    *,
    drawn_thickness: float = 0.085,
    grid: bool = True,
    labels: bool = False,
    color_x: Color | str = BRICK,
    color_y: Color | str = STEEL,
    color_concrete: Color | str = CONCRETE,
    slab_fill: Color | str = "#EFEBE3",
) -> Plan:
    """Dibuja la planta con ``width`` unidades de escena de ancho."""
    scale = width / WIDTH
    ox = center[0] - WIDTH * scale / 2
    oy = center[1] - DEPTH * scale / 2

    def p(x: float, y: float) -> tuple[float, float]:
        return ox + x * scale, oy + y * scale

    slab = (
        scene.geometry.rect(WIDTH * scale, DEPTH * scale)
        .fill(slab_fill)
        .stroke(RULE, 0.018)
        .move_to(*p(WIDTH / 2, DEPTH / 2))
        .z_index(0)
    )
    x0, y0, x1, y1 = STAIR
    void = (
        scene.geometry.rect((x1 - x0) * scale, (y1 - y0) * scale)
        .fill("#F9F7F2")
        .stroke(RULE, 0.012)
        .move_to(*p((x0 + x1) / 2, (y0 + y1) / 2))
        .z_index(0)
    )

    walls: dict[str, Drawable] = {}
    wall_labels: dict[str, Text] = {}
    thick = (
        drawn_thickness  # unidades de escena; el espesor real no se ve a esta escala
    )
    for name, wall, ax, ay, bx, by in wall_segments():
        color = (
            color_concrete
            if wall.material == "concreto"
            else (color_x if wall.direction == "X" else color_y)
        )
        length = (bx - ax + by - ay) * scale
        w, h = (length, thick) if wall.direction == "X" else (thick, length)
        walls[name] = (
            scene.geometry.rect(w, h)
            .fill(color)
            .no_stroke()
            .move_to(*p((ax + bx) / 2, (ay + by) / 2))
            .z_index(4)
        )
        if labels:
            lx, ly = p((ax + bx) / 2, (ay + by) / 2)
            if wall.direction == "X":
                ly += 0.17 if wall.fixed < DEPTH - 0.1 else -0.17
            else:
                lx += 0.2 if ax < WIDTH / 2 else -0.2
            wall_labels[name] = scene.text(
                name.replace("_2", "′"), font=MONO, size=0.13, color=INK_SOFT
            ).move_to(lx, ly, Anchor.CENTER)

    grid_lines: list[Drawable] = []
    bubbles: list[Drawable] = []
    if grid:
        ext = 0.55
        for label, gx in AXIS_X.items():
            ax_, ay_ = p(gx, 0)
            top = oy + DEPTH * scale + ext
            grid_lines.append(
                scene.geometry.dashed_line(
                    ax_, oy - 0.12, ax_, top - 0.18, dash_length=0.08, gap_length=0.06
                )
                .stroke(MUTED, 0.008)
                .z_index(2)
            )
            bubbles.append(_bubble(scene, label, ax_, top))
        for label, gy in AXIS_Y.items():
            _, by_ = p(0, gy)
            left = ox - ext
            grid_lines.append(
                scene.geometry.dashed_line(
                    left + 0.18,
                    by_,
                    ox + WIDTH * scale + 0.12,
                    by_,
                    dash_length=0.08,
                    gap_length=0.06,
                )
                .stroke(MUTED, 0.008)
                .z_index(2)
            )
            bubbles.append(_bubble(scene, label, left, by_))

    return Plan(
        slab, void, walls, grid_lines, bubbles, wall_labels, (ox, oy), scale, thick
    )


def _bubble(scene: Scene, label: str, x: float, y: float) -> Drawable:
    ring = (
        scene.geometry.circle(0.14).fill("#F9F7F2").stroke(MUTED, 0.012).move_to(x, y)
    )
    text = scene.text(label, font=MONO, size=0.12, color=INK_SOFT).move_to(
        x, y, Anchor.CENTER
    )
    return scene.geometry.group([ring, text]).z_index(3)
