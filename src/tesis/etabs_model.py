"""Modelo completo tridimensional (MCT) del caso de estudio, como se ve en ETABS.

Muros y losas son áreas (shell) sin espesor sobre los ejes; columnas y vigas, líneas
(frame) de nodo a nodo. Cada área es un grupo 2D llevado al mundo con ``in_3d()``: su
contorno y su malla se dibujan en el plano del muro, con los colores planos del sistema
visual, y la cámara en perspectiva los inclina y los oculta píxel a píxel detrás de lo
que tienen delante, sin orden del pintor. Los frames son líneas 3D entre anclas
invisibles en los nodos: al mover un ancla, sus frames la siguen.

Las coordenadas van en metros (``tesis.model3d``). ``sway`` lleva el modelo a la
deformada en Y: cada nivel se desplaza ``amplitud · modo(z)``; los muros en X giran
fuera de su plano y los muros en Y se distorsionan en el suyo, de nivel a nivel.
"""

import math
from collections.abc import Sequence
from dataclasses import dataclass, field
from itertools import pairwise
from typing import Literal

from gaanim import Anchor, Anim, Color, Drawable, Easing, EasingCurve, Material3D, Scene

from tesis.building import AXIS_X, AXIS_Y, DEPTH, STAIR, WIDTH, wall_segments
from tesis.data.planta import STORIES
from tesis.data.thesis import MESH_STEP
from tesis.kit import t
from tesis.model3d import P2, P3, anchor, lay_flat, pinned, world
from tesis.theme import CONCRETE, INK_SOFT, MONO, MUTED

SNAP = 0.07  # m: un extremo a menos de medio espesor de un eje cae sobre el eje
GRID_EXT = 0.9  # m: las grillas sobresalen de la planta hasta sus burbujas

# Colores planos de las áreas: la cara de los muros en X es más clara que la de los
# muros en Y, como la luz de la isométrica de la vivienda.
WALL_X = Color.from_hex("#EED7CA")
WALL_Y = Color.from_hex("#E3C3B2")
WALL_CONCRETE = Color.from_hex("#DCDAD5")
WALL_EDGE = Color.from_hex("#C98A70")
SLAB = Color.from_hex("#E6E3DC")
FRAME = Color.from_hex("#6E727A")
MESH = Color.from_hex("#B8532F")
SINE = Easing.ease_in_out(EasingCurve.SINE)

EDGE_WIDTH = 0.03  # m: borde de las áreas
MESH_WIDTH = 0.018  # m: líneas de la malla
FRAME_THICKNESS = 0.075  # m: diámetro de columnas y vigas
FRAME_MATERIAL = Material3D.matte(FRAME)


@dataclass(frozen=True)
class WallLine:
    """Muro en planta sobre su eje, con su etiqueta Pier (``X1_2`` es el simétrico)."""

    name: str
    direction: Literal["X", "Y"]
    concrete: bool
    a: P2
    b: P2

    @property
    def label(self) -> str:
        return self.name.replace("_2", "′")

    @property
    def middle(self) -> P2:
        return (self.a[0] + self.b[0]) / 2, (self.a[1] + self.b[1]) / 2

    @property
    def length(self) -> float:
        return math.hypot(self.b[0] - self.a[0], self.b[1] - self.a[1])


@dataclass
class Wall:
    """Un muro en un piso: grupo en su plano con el contorno y la malla.

    Las coordenadas 2D del grupo son (posición a lo largo del muro, z): x para los
    muros en X, y para los muros en Y. El grupo gira alrededor del centro del muro.
    """

    line: WallLine
    z0: float
    z1: float
    group: Drawable
    outline: Drawable
    mesh: list[Drawable]
    mesh_points: list[list[P2]]

    @property
    def span(self) -> tuple[float, float]:
        (ax, ay), (bx, by) = self.line.a, self.line.b
        return (ax, bx) if self.line.direction == "X" else (ay, by)

    @property
    def corners(self) -> list[P2]:
        u0, u1 = self.span
        return [(u0, self.z0), (u1, self.z0), (u1, self.z1), (u0, self.z1)]

    @property
    def center(self) -> P3:
        x, y = self.line.middle
        return x, y, (self.z0 + self.z1) / 2


@dataclass
class Slab:
    """Losa de un nivel: relleno, borde y vacío de escalera en el plano del nivel."""

    z: float
    group: Drawable
    fill: Drawable
    edge: Drawable
    void: Drawable


@dataclass
class Story:
    number: int
    z0: float
    z1: float
    walls: dict[str, Wall]
    columns: dict[P2, Drawable]
    beams: dict[tuple[P2, P2], Drawable]  # de nodo a nodo
    slab: Slab


@dataclass
class EtabsModel:
    lines: list[WallLine]
    nodes: list[P2]
    stories: list[Story]
    anchors: dict[tuple[P2, int], Drawable]  # (nodo, nivel): 0 es la base
    grid: Drawable  # grupo de las grillas, tendido en la base
    grid_lines: list[Drawable]
    bubbles: list[Drawable]
    # Objetos que viajan con el modelo sin deformarse, con la altura que siguen.
    riders: list[tuple[Drawable, float]] = field(default_factory=list)
    amplitude: float = 0.0

    @property
    def height(self) -> float:
        return self.stories[-1].z1

    @property
    def levels(self) -> list[float]:
        return [0.0, *(s.z1 for s in self.stories)]

    def walls(self) -> list[Wall]:
        return [w for s in self.stories for w in s.walls.values()]

    def ride(self, drawable: Drawable, z: float) -> Drawable:
        """Registra un objeto 3D que acompaña a la deformada a la altura ``z``."""
        self.riders.append((drawable, z))
        return drawable

    def mode(self, z: float) -> float:
        """Forma esquemática del modo de traslación: un cuarto de seno en altura."""
        return math.sin(math.pi * z / (2 * self.height))

    def sway(self, amplitude: float, duration: float) -> list[Anim]:
        """Lleva el modelo a la deformada en Y con ``amplitude`` metros en la azotea.

        Cada tipo de pieza se mueve a su manera (gaanim #702).
        """

        def ease(anim: Anim) -> Anim:
            return anim.duration(duration).easing(SINE)

        def shift(z: float) -> float:
            return amplitude * self.mode(z)

        def change(z: float) -> P3:
            """Desplazamiento desde la deformada anterior, en el mundo."""
            return world(0, shift(z) - self.amplitude * self.mode(z), 0)

        anims: list[Anim] = []
        levels = self.levels
        for ((x, y), level), point in self.anchors.items():
            if level:
                z = levels[level]
                anims.append(ease(point.animate.move_to_3d(*world(x, y + shift(z), z))))
        for wall in self.walls():
            d0, d1 = shift(wall.z0), shift(wall.z1)
            if wall.line.direction == "X":
                # Fuera de su plano: el muro se corre y se inclina entre los dos niveles.
                x, y, zc = wall.center
                tilt = -math.asin((d1 - d0) / (wall.z1 - wall.z0))
                anims.append(
                    ease(wall.group.animate.move_to_3d(*world(x, y + shift(zc), zc)))
                )
                anims.append(ease(wall.group.animate.rotate_to_3d(tilt, 0, 0)))
            else:
                # En su plano: cada punto avanza lo que avanza su altura.
                def drift(u: float, h: float, w: Wall = wall) -> P2:
                    s = (h - w.z0) / (w.z1 - w.z0)
                    return u + d0 + (d1 - d0) * s, h

                anims.append(
                    ease(wall.outline.animate.points([drift(*p) for p in wall.corners]))
                )
                for part, pts in zip(wall.mesh, wall.mesh_points, strict=True):
                    anims.append(ease(part.animate.points([drift(*p) for p in pts])))
        for story in self.stories:
            slab = world(0, shift(story.z1), story.z1)
            anims.append(ease(story.slab.group.animate.move_to_3d(*slab)))
        # Los acompañantes se corren desde la deformada anterior: aquí solo se conoce
        # su altura, no su posición.
        for drawable, z in self.riders:
            anims.append(ease(drawable.animate.shift_by_3d(*change(z))))
        self.amplitude = amplitude
        return anims


def _snap(value: float, axes: Sequence[float], top: float) -> float:
    value = min(max(value, 0.0), top)
    for axis in axes:
        if abs(value - axis) <= SNAP:
            return axis
    return value


def wall_lines() -> list[WallLine]:
    """Muros sobre sus ejes: los extremos con media columna se llevan al eje vecino."""
    xs, ys = list(AXIS_X.values()), list(AXIS_Y.values())
    lines: list[WallLine] = []
    for name, wall, x0, y0, x1, y1 in wall_segments():
        a = (_snap(x0, xs, WIDTH), _snap(y0, ys, DEPTH))
        b = (_snap(x1, xs, WIDTH), _snap(y1, ys, DEPTH))
        lines.append(WallLine(name, wall.direction, wall.material == "concreto", a, b))
    return lines


def mesh_paths(u0: float, u1: float, z0: float, z1: float) -> list[list[P2]]:
    """Malla de un muro como dos serpentinas: las filas y las columnas interiores.

    Los tramos que unen una línea con la siguiente corren por los bordes del muro, que
    ya son vigas y columnas, así que dos polilíneas dibujan toda la malla.
    """
    nu = max(1, math.ceil(abs(u1 - u0) / MESH_STEP - 1e-6))
    nz = max(1, math.ceil((z1 - z0) / MESH_STEP - 1e-6))
    rows: list[P2] = []
    for j in range(1, nz):
        z = z0 + (z1 - z0) * j / nz
        ends = (u0, u1) if j % 2 else (u1, u0)
        rows += [(ends[0], z), (ends[1], z)]
    cols: list[P2] = []
    for i in range(1, nu):
        u = u0 + (u1 - u0) * i / nu
        ends = (z0, z1) if i % 2 else (z1, z0)
        cols += [(u, ends[0]), (u, ends[1])]
    return [path for path in (rows, cols) if len(path) >= 2]


def _split(a: P2, b: P2, nodes: Sequence[P2]) -> list[tuple[P2, P2]]:
    """Tramos de una línea de vigas entre nodos consecutivos (frames de nodo a nodo)."""
    if a[1] == b[1]:
        cut = sorted({p[0] for p in nodes if p[1] == a[1] and a[0] <= p[0] <= b[0]})
        stops = [(x, a[1]) for x in sorted({a[0], b[0], *cut})]
    else:
        cut = sorted({p[1] for p in nodes if p[0] == a[0] and a[1] <= p[1] <= b[1]})
        stops = [(a[0], y) for y in sorted({a[1], b[1], *cut})]
    return list(pairwise(stops))


def slab_outline() -> list[P2]:
    """Losa con el vacío de escalera: el vacío se recorre al revés, unido por una ranura."""
    x0, y0, x1, y1 = STAIR
    return [
        (0, 0),
        (x0, 0),
        (x0, y0),
        (x0, y1),
        (x1, y1),
        (x1, y0),
        (x0, y0),
        (x0, 0),
        (WIDTH, 0),
        (WIDTH, DEPTH),
        (0, DEPTH),
    ]


def rect(x0: float, y0: float, x1: float, y1: float) -> list[P2]:
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def stand(drawable: Drawable, line: WallLine, z: float) -> Drawable:
    """Levanta sobre el eje de ``line`` un objeto 2D dibujado en (u, z), en metros.

    u es x para un muro en X e y para un muro en Y; el grupo debe tener su origen en
    el centro del muro, (u_c, z), que queda sobre el punto medio del eje a la altura z
    (gaanim #703).
    """
    x, y = line.middle
    drawable.in_3d().move_to_3d(*world(x, y, z))
    if line.direction == "Y":
        drawable.rotate_to_3d(0, math.pi / 2, 0)
    return drawable


def _wall(scene: Scene, line: WallLine, z0: float, z1: float) -> Wall:
    (ax, ay), (bx, by) = line.a, line.b
    u0, u1 = (ax, bx) if line.direction == "X" else (ay, by)
    fill = (
        WALL_CONCRETE
        if line.concrete
        else (WALL_X if line.direction == "X" else WALL_Y)
    )
    edge = CONCRETE if line.concrete else WALL_EDGE
    outline = (
        scene.geometry.polygon(rect(u0, z0, u1, z1))
        .fill(fill)
        .stroke(edge, EDGE_WIDTH)
        .hidden()
    )
    paths = mesh_paths(u0, u1, z0, z1)
    mesh = [
        scene.geometry.polyline(path)
        .no_fill()
        .stroke(CONCRETE if line.concrete else MESH, MESH_WIDTH)
        .opacity(0.55)
        .hidden()
        for path in paths
    ]
    zc = (z0 + z1) / 2
    group = scene.geometry.group([outline, *mesh], origin=((u0 + u1) / 2, zc))
    stand(group, line, zc)
    return Wall(line, z0, z1, group, outline, mesh, paths)


def _slab(scene: Scene, z: float) -> Slab:
    x0, y0, x1, y1 = STAIR
    fill = scene.geometry.polygon(slab_outline()).fill(SLAB).no_stroke().hidden()
    edge = (
        scene.geometry.polygon(rect(0, 0, WIDTH, DEPTH))
        .no_fill()
        .stroke(MUTED, EDGE_WIDTH)
        .hidden()
    )
    void = (
        scene.geometry.polygon(rect(x0, y0, x1, y1))
        .no_fill()
        .stroke(MUTED, EDGE_WIDTH * 0.8)
        .hidden()
    )
    group = scene.geometry.group([fill, edge, void], origin=(0, 0))
    lay_flat(group, z)
    return Slab(z, group, fill, edge, void)


def frame_line(scene: Scene, start: Drawable, end: Drawable) -> Drawable:
    """Frame entre dos anclas: crece de ``start`` a ``end`` y las sigue si se mueven."""
    return scene.geometry.line_3d(
        start, end, FRAME_THICKNESS, segments=10, material=FRAME_MATERIAL
    ).hidden()


def build_model(scene: Scene) -> EtabsModel:
    """Crea todo el modelo oculto; cada paso de la diapositiva decide cuándo aparece."""
    lines = wall_lines()
    nodes = sorted({p for line in lines for p in (line.a, line.b)})

    # Vigas: las del perímetro corren de esquina a esquina; adentro, sobre cada muro.
    perimeter: list[tuple[P2, P2]] = [
        ((0, 0), (WIDTH, 0)),
        ((WIDTH, 0), (WIDTH, DEPTH)),
        ((0, DEPTH), (WIDTH, DEPTH)),
        ((0, 0), (0, DEPTH)),
    ]

    def on_perimeter(line: WallLine) -> bool:
        (ax, ay), (bx, by) = line.a, line.b
        return (ay == by and ay in (0, DEPTH)) or (ax == bx and ax in (0, WIDTH))

    beam_lines = perimeter + [(ln.a, ln.b) for ln in lines if not on_perimeter(ln)]
    spans = sorted({span for a, b in beam_lines for span in _split(a, b, nodes)})
    span_nodes = sorted({p for span in spans for p in span})

    levels = [level for _, level in STORIES]
    anchors: dict[tuple[P2, int], Drawable] = {
        (node, k): anchor(scene, (*node, z))
        for k, z in enumerate(levels)
        for node in sorted({*nodes, *span_nodes})
    }
    stories: list[Story] = []
    for number, (z0, z1) in enumerate(pairwise(levels), start=1):
        walls = {line.name: _wall(scene, line, z0, z1) for line in lines}
        columns = {
            node: frame_line(scene, anchors[node, number - 1], anchors[node, number])
            for node in nodes
        }
        beams = {
            (a, b): frame_line(scene, anchors[a, number], anchors[b, number])
            for a, b in spans
        }
        stories.append(Story(number, z0, z1, walls, columns, beams, _slab(scene, z1)))

    grid_lines: list[Drawable] = []
    bubbles: list[Drawable] = []
    for name, gx in AXIS_X.items():
        grid_lines.append(_dashed(scene, (gx, -GRID_EXT + 0.12), (gx, DEPTH + 0.5)))
        bubbles.append(_bubble(scene, name, (gx, -GRID_EXT, 0)))
    for name, gy in AXIS_Y.items():
        grid_lines.append(_dashed(scene, (-GRID_EXT + 0.12, gy), (WIDTH + 0.5, gy)))
        bubbles.append(_bubble(scene, name, (-GRID_EXT, gy, 0)))
    grid = lay_flat(scene.geometry.group(grid_lines, origin=(0, 0)), -0.01)
    return EtabsModel(lines, nodes, stories, anchors, grid, grid_lines, bubbles)


def _dashed(scene: Scene, a: P2, b: P2) -> Drawable:
    return (
        scene.geometry.dashed_line(*a, *b, dash_length=0.24, gap_length=0.18)
        .stroke(MUTED, 0.028)
        .hidden()
    )


def _bubble(scene: Scene, name: str, at: P3) -> Drawable:
    """Burbuja de grilla: siempre de frente a la cámara, al pie de su eje."""
    ring = scene.geometry.circle(0.105).fill("#F9F7F2").stroke(MUTED, 0.01)
    text = t(
        scene, name, 0, 0, font=MONO, size=0.1, color=INK_SOFT, anchor=Anchor.CENTER
    )
    return pinned(scene.geometry.group([ring, text]), at, anchor=Anchor.CENTER)
