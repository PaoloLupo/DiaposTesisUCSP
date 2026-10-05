"""Modelo completo tridimensional (MCT) del caso de estudio, como se ve en ETABS.

Muros y losas son áreas (shell) sin espesor sobre los ejes; columnas y vigas, líneas
(frame) de nodo a nodo. La isométrica es la de ``tesis.vivienda``: se ven las caras
que miran a −y, a +x y a +z, y un punto queda más cerca del observador cuanto mayor
es ``x − y + z``. Los pisos se pintan de abajo hacia arriba; dentro de cada piso,
muros y columnas de atrás hacia adelante y, al final, la losa con sus vigas encima.

Cada forma guarda sus vértices en metros: ``sway`` lleva cada vértice a la deformada
según la altura de su nivel.
"""

import math
from collections.abc import Sequence
from dataclasses import dataclass, field
from itertools import pairwise
from typing import Literal

from gaanim import Anchor, Anim, Color, Drawable, Easing, EasingCurve, Scene

from tesis.building import AXIS_X, AXIS_Y, DEPTH, STAIR, WIDTH, wall_segments
from tesis.data.planta import STORIES
from tesis.data.thesis import MESH_STEP
from tesis.kit import t
from tesis.theme import CONCRETE, INK_SOFT, MONO, MUTED
from tesis.vivienda import Iso

type P2 = tuple[float, float]
type P3 = tuple[float, float, float]

SNAP = 0.07  # m: un extremo a menos de medio espesor de un eje cae sobre el eje
GRID_EXT = 0.9  # m: las grillas sobresalen de la planta hasta sus burbujas

# Sombreado plano, como en la vivienda: la cara que mira a −y es más clara que la de +x.
WALL_X = Color.from_hex("#EED7CA")
WALL_Y = Color.from_hex("#E3C3B2")
WALL_CONCRETE = Color.from_hex("#DCDAD5")
WALL_EDGE = Color.from_hex("#C98A70")
SLAB = Color.from_hex("#E6E3DC")
FRAME = Color.from_hex("#6E727A")
MESH = Color.from_hex("#B8532F")
SINE = Easing.ease_in_out(EasingCurve.SINE)
# El modelo ocupa z_index de 10 a unos 400; lo que va encima parte de aquí.
OVERLAY = 1000


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


@dataclass
class Shape:
    """Polígono o polilínea con sus vértices en metros, para deformarlo después."""

    drawable: Drawable
    points: list[P3]


@dataclass
class Story:
    number: int
    z0: float
    z1: float
    walls: dict[str, Shape]
    mesh: dict[str, list[Shape]]
    columns: dict[P2, Shape]
    beams: dict[tuple[P2, P2], Shape]  # de nodo a nodo
    slab: Shape
    edge: Shape  # borde de la losa: es el nivel que sube al definir los pisos
    void: Shape  # borde del vacío de escalera
    overlay: int  # z_index libre para lo que se dibuje sobre este nivel


@dataclass
class EtabsModel:
    iso: Iso
    lines: list[WallLine]
    stories: list[Story]
    grid: list[Drawable]
    bubbles: list[Drawable]
    # Objetos que viajan con el modelo sin deformarse, con la altura que siguen.
    riders: list[tuple[Drawable, float]] = field(default_factory=list)
    amplitude: float = 0.0

    @property
    def height(self) -> float:
        return self.stories[-1].z1

    def shapes(self) -> list[Shape]:
        out: list[Shape] = []
        for story in self.stories:
            out += list(story.walls.values())
            out += [m for parts in story.mesh.values() for m in parts]
            out += list(story.columns.values())
            out += list(story.beams.values())
            out += [story.slab, story.edge, story.void]
        return out

    def ride(self, drawable: Drawable, z: float) -> Drawable:
        """Registra un objeto que acompaña a la deformada a la altura ``z``."""
        self.riders.append((drawable, z))
        return drawable

    def mode(self, z: float) -> float:
        """Forma esquemática del modo de traslación: un cuarto de seno en altura."""
        return math.sin(math.pi * z / (2 * self.height))

    def sway(self, amplitude: float, duration: float) -> list[Anim]:
        """Lleva el modelo a la deformada en Y con ``amplitude`` metros en la azotea."""
        anims = [
            s.drawable.animate.points(
                [self.iso(x, y + amplitude * self.mode(z), z) for x, y, z in s.points]
            )
            .duration(duration)
            .easing(SINE)
            for s in self.shapes()
        ]
        for drawable, z in self.riders:
            dx, dy = self.iso.along(0, (amplitude - self.amplitude) * self.mode(z))
            anims.append(
                drawable.animate.shift_by(dx, dy).duration(duration).easing(SINE)
            )
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


def _depth(a: P2, b: P2, u: float) -> float:
    """``x − y`` del punto del elemento que se proyecta en ``u = x + y``; mayor = más cerca."""
    ua, ub = a[0] + a[1], b[0] + b[1]
    da, db = a[0] - a[1], b[0] - b[1]
    if abs(ub - ua) < 1e-9:
        return da
    return da + (u - ua) / (ub - ua) * (db - da)


def back_to_front(items: Sequence[tuple[P2, P2]]) -> list[int]:
    """Orden del pintor para muros (segmentos) y columnas (puntos) de un mismo piso.

    Dos elementos solo se ordenan si se solapan en pantalla (en ``x + y``); entonces
    va primero el más lejano. Una columna en el extremo de un muro va encima de él.
    """
    n = len(items)
    spans = [sorted((a[0] + a[1], b[0] + b[1])) for a, b in items]
    later: list[set[int]] = [set() for _ in range(n)]
    pending = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            lo = max(spans[i][0], spans[j][0])
            hi = min(spans[i][1], spans[j][1])
            if hi < lo - 1e-9:
                continue
            u = (lo + hi) / 2
            di, dj = _depth(*items[i], u), _depth(*items[j], u)
            if abs(di - dj) < 1e-6:
                point_i = items[i][0] == items[i][1]
                point_j = items[j][0] == items[j][1]
                if point_i == point_j:
                    continue
                first, second = (j, i) if point_i else (i, j)
            else:
                first, second = (i, j) if di < dj else (j, i)
            if second not in later[first]:
                later[first].add(second)
                pending[second] += 1

    def mean_depth(k: int) -> float:
        (ax, ay), (bx, by) = items[k]
        return (ax - ay + bx - by) / 2

    order: list[int] = []
    ready = [k for k in range(n) if pending[k] == 0]
    while ready:
        ready.sort(key=mean_depth)
        k = ready.pop(0)
        order.append(k)
        for m in later[k]:
            pending[m] -= 1
            if pending[m] == 0:
                ready.append(m)
    # Sin ciclos entre segmentos que no se cruzan; por si acaso, el resto por profundidad.
    order += sorted((k for k in range(n) if k not in order), key=mean_depth)
    return order


def _mesh_paths(line: WallLine, z0: float, z1: float) -> list[list[P3]]:
    """Malla del muro como dos serpentinas: las filas y las columnas interiores.

    Los tramos que unen una línea con la siguiente corren por los bordes del muro, que
    ya son vigas y columnas, así que dos polilíneas dibujan toda la malla.
    """
    (ax, ay), (bx, by) = line.a, line.b
    length = math.hypot(bx - ax, by - ay)
    nu = max(1, math.ceil(length / MESH_STEP - 1e-6))
    nz = max(1, math.ceil((z1 - z0) / MESH_STEP - 1e-6))

    def p(s: float, z: float) -> P3:
        return ax + (bx - ax) * s, ay + (by - ay) * s, z

    rows: list[P3] = []
    for j in range(1, nz):
        z = z0 + (z1 - z0) * j / nz
        ends = (0.0, 1.0) if j % 2 else (1.0, 0.0)
        rows += [p(ends[0], z), p(ends[1], z)]
    cols: list[P3] = []
    for i in range(1, nu):
        s = i / nu
        ends = (z0, z1) if i % 2 else (z1, z0)
        cols += [p(s, ends[0]), p(s, ends[1])]
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


def _slab_points(z: float) -> list[P3]:
    """Losa con el vacío de escalera: el vacío se recorre al revés, unido por una ranura."""
    x0, y0, x1, y1 = STAIR
    return [
        (0, 0, z),
        (x0, 0, z),
        (x0, y0, z),
        (x0, y1, z),
        (x1, y1, z),
        (x1, y0, z),
        (x0, y0, z),
        (x0, 0, z),
        (WIDTH, 0, z),
        (WIDTH, DEPTH, z),
        (0, DEPTH, z),
    ]


def build_model(scene: Scene, iso: Iso, *, z_base: int = 10) -> EtabsModel:
    """Crea todo el modelo oculto; cada paso de la diapositiva decide cuándo aparece."""
    lines = wall_lines()
    nodes = sorted({p for line in lines for p in (line.a, line.b)})
    items: list[tuple[P2, P2]] = [(line.a, line.b) for line in lines]
    items += [(p, p) for p in nodes]
    order = back_to_front(items)

    def polygon(points: list[P3]) -> Drawable:
        return scene.geometry.polygon([iso(*p) for p in points]).hidden()

    def polyline(points: list[P3]) -> Drawable:
        return scene.geometry.polyline([iso(*p) for p in points]).no_fill().hidden()

    def outline(points: list[P3]) -> Drawable:
        """Contorno cerrado: un polígono sin relleno admite ``points`` como el muro."""
        return polygon(points).no_fill()

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

    z = z_base
    stories: list[Story] = []
    levels = [level for _, level in STORIES]
    for number, (z0, z1) in enumerate(pairwise(levels), start=1):
        walls: dict[str, Shape] = {}
        mesh: dict[str, list[Shape]] = {}
        columns: dict[P2, Shape] = {}
        for k in order:
            if k < len(lines):
                line = lines[k]
                pts: list[P3] = [
                    (*line.a, z0),
                    (*line.b, z0),
                    (*line.b, z1),
                    (*line.a, z1),
                ]
                fill = (
                    WALL_CONCRETE
                    if line.concrete
                    else (WALL_X if line.direction == "X" else WALL_Y)
                )
                edge = CONCRETE if line.concrete else WALL_EDGE
                walls[line.name] = Shape(
                    polygon(pts).fill(fill).stroke(edge, 0.008).z_index(z), pts
                )
                mesh[line.name] = [
                    Shape(
                        polyline(path)
                        .stroke(CONCRETE if line.concrete else MESH, 0.0045)
                        .opacity(0.55)
                        .z_index(z + 1),
                        path,
                    )
                    for path in _mesh_paths(line, z0, z1)
                ]
                z += 2
            else:
                node = nodes[k - len(lines)]
                pts = [(*node, z0), (*node, z1)]
                columns[node] = Shape(
                    polyline(pts).stroke(FRAME, 0.016).z_index(z), pts
                )
                z += 1
        slab_pts = _slab_points(z1)
        slab = Shape(polygon(slab_pts).fill(SLAB).no_stroke().z_index(z), slab_pts)
        edge_pts: list[P3] = [
            (0, 0, z1),
            (WIDTH, 0, z1),
            (WIDTH, DEPTH, z1),
            (0, DEPTH, z1),
        ]
        edge = Shape(outline(edge_pts).stroke(MUTED, 0.01).z_index(z + 1), edge_pts)
        x0, y0, x1, y1 = STAIR
        void_pts: list[P3] = [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
        void = Shape(
            outline(void_pts).stroke(MUTED, 0.008).z_index(z + 1),
            void_pts,
        )
        beams: dict[tuple[P2, P2], Shape] = {}
        for a, b in spans:
            pts = [(*a, z1), (*b, z1)]
            beams[a, b] = Shape(polyline(pts).stroke(FRAME, 0.016).z_index(z + 2), pts)
        stories.append(
            Story(number, z0, z1, walls, mesh, columns, beams, slab, edge, void, z + 3)
        )
        z += 4

    assert z < OVERLAY, z
    grid: list[Drawable] = []
    bubbles: list[Drawable] = []
    for name, gx in AXIS_X.items():
        a, b = iso(gx, -GRID_EXT + 0.12, 0), iso(gx, DEPTH + 0.5, 0)
        grid.append(_dashed(scene, a, b))
        bubbles.append(_bubble(scene, name, *iso(gx, -GRID_EXT, 0)))
    for name, gy in AXIS_Y.items():
        a, b = iso(-GRID_EXT + 0.12, gy, 0), iso(WIDTH + 0.5, gy, 0)
        grid.append(_dashed(scene, a, b))
        bubbles.append(_bubble(scene, name, *iso(-GRID_EXT, gy, 0)))
    return EtabsModel(iso, lines, stories, grid, bubbles)


def _dashed(scene: Scene, a: P2, b: P2) -> Drawable:
    return (
        scene.geometry.dashed_line(*a, *b, dash_length=0.06, gap_length=0.045)
        .stroke(MUTED, 0.007)
        .z_index(2)
        .hidden()
    )


def _bubble(scene: Scene, name: str, x: float, y: float) -> Drawable:
    ring = (
        scene.geometry.circle(0.105).fill("#F9F7F2").stroke(MUTED, 0.01).move_to(x, y)
    )
    text = t(
        scene, name, x, y, font=MONO, size=0.1, color=INK_SOFT, anchor=Anchor.CENTER
    )
    return scene.geometry.group([ring, text]).z_index(3).hidden()
