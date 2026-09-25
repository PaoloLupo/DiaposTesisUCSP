"""Vivienda de albañilería confinada en isométrica, dibujada en 2D.

Modelo en metros: x a lo largo de la fachada, y en profundidad, z hacia arriba.
La proyección deja ver las caras que miran a −y (fachada), a +x (costado
derecho) y a +z (techo). Todo se dibuja por hiladas, de abajo hacia arriba, y
dentro de cada hilada de atrás hacia adelante: a lo largo de un rayo de vista lo
más cercano está siempre más alto, así que ese orden resuelve las oclusiones y
permite deformar la vivienda por corte moviendo cada hilada según su altura.
"""

import math
from dataclasses import dataclass
from typing import Literal, NamedTuple

from gaanim import Color, Drawable, Scene

from tesis.theme import BRICK, CONCRETE_SOFT, PAPER_DEEP, RULE

LX, LY = 6.0, 4.2  # planta, m
T = 0.15  # espesor del muro de soga
COL = 0.25  # lado de la columna a lo largo del muro
DOOR = (3.6, 4.5)  # vano de la puerta en la fachada
WINDOW = (1.5, 2.7)  # vano de la ventana en el muro derecho
Z_FOUND = 0.2  # cimiento corrido
Z_BASE = 0.4  # sobrecimiento: arranque del muro
Z_TOP = 2.8  # última hilada
Z_ROOF = 3.0  # viga solera y losa
COURSES = 23
COURSE = (Z_TOP - Z_BASE) / COURSES
# Vanos por hiladas: alféizar 0–8, ventana 9–18, puerta 0–18, dintel 19–20 y
# dos hiladas de muro sobre el dintel.
SILL, LINTEL, ABOVE = 9, 19, 21
BRICK_PITCH = 0.25  # ladrillo con junta
JOINT = 0.014
TOOTH = 0.08  # dentado, exagerado para que se lea a esta escala
INSET = 0.045  # recubrimiento del acero

# Sombreado plano: techo claro, fachada media, costado oscuro.
BRICK_FRONT = BRICK
BRICK_SIDE = Color.from_hex("#97421F")
BRICK_TOP = Color.from_hex("#CC7A57")
MORTAR_FRONT = Color.from_hex("#D8CDBF")
MORTAR_SIDE = Color.from_hex("#BFB3A4")
CONCRETE_TOP = CONCRETE_SOFT
CONCRETE_FRONT = Color.from_hex("#D2D0CB")
CONCRETE_SIDE = Color.from_hex("#B9B7B1")
STEEL_BAR = Color.from_hex("#4E535C")

type Point3 = tuple[float, float, float]
type Axis = Literal["x", "y"]
ALL = (0, COURSES)


def toothed(course: int) -> bool:
    """En hiladas alternas el ladrillo extremo entra en la columna."""
    return course % 2 == 0


@dataclass(frozen=True)
class Iso:
    origin: tuple[float, float]
    scale: float

    def __call__(self, x: float, y: float, z: float) -> tuple[float, float]:
        ox, oy = self.origin
        c = math.cos(math.pi / 6)
        return ox + (x + y) * c * self.scale, oy + ((y - x) * 0.5 + z) * self.scale

    def along(self, dx: float, dy: float) -> tuple[float, float]:
        """Desplazamiento en pantalla de un vector horizontal del modelo."""
        c = math.cos(math.pi / 6)
        return (dx + dy) * c * self.scale, (dy - dx) * 0.5 * self.scale


class Face(NamedTuple):
    """Cara expuesta de una columna; ``tooth`` indica de qué lado entra el muro."""

    axis: Axis
    plane: float
    a0: float
    a1: float
    tooth: Literal["low", "high", ""] = ""
    courses: tuple[int, int] = ALL


@dataclass(frozen=True)
class Column:
    x0: float
    x1: float
    y0: float
    y1: float
    faces: tuple[Face, ...]

    @property
    def bars(self) -> list[tuple[float, float]]:
        pts = [
            (x, y)
            for x in (self.x0 + INSET, self.x1 - INSET)
            for y in (self.y0 + INSET, self.y1 - INSET)
        ]
        return sorted(pts, key=lambda p: p[0] - p[1])  # de atrás hacia adelante


@dataclass(frozen=True)
class Panel:
    direction: Literal["X", "Y"]
    plane: float  # coordenada de la cara visible
    back: float  # coordenada de la cara opuesta
    start: float
    end: float
    teeth: tuple[bool, bool] = (False, False)  # dentado al inicio y al final
    courses: tuple[int, int] = ALL


@dataclass(frozen=True)
class Lintel:
    """Dintel de concreto sobre un vano: solo su cara visible."""

    axis: Axis
    plane: float
    a0: float
    a1: float


# Orden de dibujo dentro de cada hilada, de atrás hacia adelante.
ELEMENTS: tuple[Column | Panel | Lintel, ...] = (
    Column(
        0,
        COL,
        LY - COL,
        LY,
        (Face("y", LY - COL, T, COL), Face("x", COL, LY - COL, LY - T)),
    ),
    Panel("X", LY - T, LY, COL, LX - COL),  # fondo, cara interior
    Panel("Y", T, 0, COL, LY - COL),  # izquierda, cara interior
    Column(
        LX - COL,
        LX,
        LY - COL,
        LY,
        (Face("y", LY - COL, LX - COL, LX - T), Face("x", LX, LY - COL, LY, "low")),
    ),
    Column(0, COL, 0, COL, (Face("y", 0, 0, COL, "high"), Face("x", COL, T, COL))),
    # Muro derecho, de atrás hacia adelante, con la ventana entre dos columnas.
    Panel("Y", LX, LX - T, WINDOW[1] + COL, LY - COL, (True, True)),
    Column(
        LX - T,
        LX,
        WINDOW[1],
        WINDOW[1] + COL,
        (
            Face("y", WINDOW[1], LX - T, LX, courses=(SILL, LINTEL)),
            Face("x", LX, WINDOW[1], WINDOW[1] + COL, "high"),
        ),
    ),
    Panel("Y", LX, LX - T, *WINDOW, courses=(0, SILL)),  # alféizar
    Lintel("x", LX, *WINDOW),
    Panel("Y", LX, LX - T, *WINDOW, courses=(ABOVE, COURSES)),
    Column(
        LX - T,
        LX,
        WINDOW[0] - COL,
        WINDOW[0],
        (Face("x", LX, WINDOW[0] - COL, WINDOW[0], "low"),),
    ),
    Panel("Y", LX, LX - T, COL, WINDOW[0] - COL, (True, True)),
    # Fachada, de izquierda a derecha, con la puerta entre dos columnas.
    Panel("X", 0, T, COL, DOOR[0] - COL, (True, True)),
    Column(
        DOOR[0] - COL,
        DOOR[0],
        0,
        T,
        (
            Face("y", 0, DOOR[0] - COL, DOOR[0], "low"),
            Face("x", DOOR[0], 0, T, courses=(0, LINTEL)),
        ),
    ),
    Lintel("y", 0, *DOOR),
    Panel("X", 0, T, *DOOR, courses=(ABOVE, COURSES)),
    Column(
        DOOR[1], DOOR[1] + COL, 0, T, (Face("y", 0, DOOR[1], DOOR[1] + COL, "high"),)
    ),
    Panel("X", 0, T, DOOR[1] + COL, LX - COL, (True, True)),
    Column(
        LX - COL,
        LX,
        0,
        COL,
        (Face("y", 0, LX - COL, LX, "low"), Face("x", LX, 0, COL, "high")),
    ),
)


@dataclass
class House:
    iso: Iso
    ground: Drawable
    footing: list[Drawable]  # cimiento corrido
    plinth: list[Drawable]  # sobrecimiento
    steel: list[Drawable]  # un grupo por hilada, y el remate sobre el muro al final
    masonry: list[Drawable]  # un grupo por hilada, con los dinteles
    tops: list[Drawable]  # cara superior provisional de cada hilada
    concrete: list[Drawable]  # columnas, un grupo por hilada
    beams: list[Drawable]
    slab: Drawable
    slab_mask: Drawable
    # Grupos que se desplazan juntos en el sismo, con su fracción de la deriva.
    layers: list[tuple[Drawable, float]]


def _poly(scene: Scene, iso: Iso, pts: list[Point3], color: Color) -> Drawable:
    return scene.geometry.polygon([iso(*p) for p in pts]).fill(color).no_stroke()


def _face(
    scene: Scene,
    iso: Iso,
    axis: Axis,
    plane: float,
    a0: float,
    a1: float,
    z0: float,
    z1: float,
    color: Color,
) -> Drawable:
    if axis == "y":
        pts = [(a0, plane, z0), (a1, plane, z0), (a1, plane, z1), (a0, plane, z1)]
    else:
        pts = [(plane, a0, z0), (plane, a1, z0), (plane, a1, z1), (plane, a0, z1)]
    return _poly(scene, iso, pts, color)


def _top(
    scene: Scene,
    iso: Iso,
    x0: float,
    x1: float,
    y0: float,
    y1: float,
    z: float,
    color: Color,
) -> Drawable:
    return _poly(
        scene, iso, [(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)], color
    )


def _ring(
    scene: Scene,
    iso: Iso,
    outer: tuple[float, float, float, float],
    inner: tuple[float, float, float, float],
    z0: float,
    z1: float,
) -> list[Drawable]:
    """Anillo de concreto (cimiento o sobrecimiento) con sus caras visibles."""
    x0, x1, y0, y1 = outer
    i0, i1, j0, j1 = inner
    return [
        _face(
            scene, iso, "y", j1, i0, i1, z0, z1, CONCRETE_FRONT
        ),  # cara interior del fondo
        _face(
            scene, iso, "x", i0, j0, j1, z0, z1, CONCRETE_SIDE
        ),  # cara interior izquierda
        _top(scene, iso, x0, x1, y0, j0, z1, CONCRETE_TOP),
        _top(scene, iso, x0, x1, j1, y1, z1, CONCRETE_TOP),
        _top(scene, iso, x0, i0, j0, j1, z1, CONCRETE_TOP),
        _top(scene, iso, i1, x1, j0, j1, z1, CONCRETE_TOP),
        _face(scene, iso, "y", y0, x0, x1, z0, z1, CONCRETE_FRONT),
        _face(scene, iso, "x", x1, y0, y1, z0, z1, CONCRETE_SIDE),
    ]


def _course_z(course: int) -> tuple[float, float]:
    z0 = Z_BASE + course * COURSE
    return z0, z0 + COURSE


def _panel_course(
    scene: Scene, iso: Iso, panel: Panel, course: int
) -> tuple[list[Drawable], Drawable]:
    """Mortero y ladrillos de la cara visible de un paño, y su cara superior."""
    z0, z1 = _course_z(course)
    s0 = panel.start - (TOOTH if panel.teeth[0] and toothed(course) else 0)
    s1 = panel.end + (TOOTH if panel.teeth[1] and toothed(course) else 0)
    axis: Axis = "y" if panel.direction == "X" else "x"
    front = panel.direction == "X"
    parts = [
        _face(
            scene,
            iso,
            axis,
            panel.plane,
            s0,
            s1,
            z0,
            z1,
            MORTAR_FRONT if front else MORTAR_SIDE,
        )
    ]
    s = s0 - (BRICK_PITCH / 2 if course % 2 else 0)
    while s < s1 - 0.02:
        a, b = max(s, s0), min(s + BRICK_PITCH, s1)
        if b - a > 0.05:
            parts.append(
                _face(
                    scene,
                    iso,
                    axis,
                    panel.plane,
                    a + JOINT / 2,
                    b - JOINT / 2,
                    z0 + JOINT / 2,
                    z1 - JOINT / 2,
                    BRICK_FRONT if front else BRICK_SIDE,
                )
            )
        s += BRICK_PITCH
    lo, hi = sorted((panel.plane, panel.back))
    if panel.direction == "X":
        top = _top(scene, iso, s0, s1, lo, hi, z1, BRICK_TOP)
    else:
        top = _top(scene, iso, lo, hi, s0, s1, z1, BRICK_TOP)
    return parts, top


def _column_course(
    scene: Scene, iso: Iso, column: Column, course: int
) -> list[Drawable]:
    z0, z1 = _course_z(course)
    parts: list[Drawable] = []
    for face in column.faces:
        if not face.courses[0] <= course < face.courses[1]:
            continue
        a0, a1 = face.a0, face.a1
        if toothed(course) and face.tooth == "low":
            a0 += TOOTH
        elif toothed(course) and face.tooth == "high":
            a1 -= TOOTH
        color = CONCRETE_FRONT if face.axis == "y" else CONCRETE_SIDE
        parts.append(_face(scene, iso, face.axis, face.plane, a0, a1, z0, z1, color))
    if course == COURSES - 1:
        parts.append(
            _top(
                scene, iso, column.x0, column.x1, column.y0, column.y1, z1, CONCRETE_TOP
            )
        )
    return parts


def _steel(
    scene: Scene, iso: Iso, column: Column, z0: float, z1: float
) -> list[Drawable]:
    parts = [
        scene.geometry.line(iso(x, y, z0), iso(x, y, z1)).stroke(STEEL_BAR, 0.012)
        for x, y in column.bars
    ]
    # Estribos cada 0.2 m desde 0.1 m sobre el sobrecimiento.
    a0, a1 = column.x0 + INSET, column.x1 - INSET
    b0, b1 = column.y0 + INSET, column.y1 - INSET
    for i in range(12):
        z = Z_BASE + 0.1 + 0.2 * i
        if z0 <= z < z1:
            ring = [
                iso(a0, b0, z),
                iso(a1, b0, z),
                iso(a1, b1, z),
                iso(a0, b1, z),
                iso(a0, b0, z),
            ]
            parts.append(
                scene.geometry.polyline(ring).no_fill().stroke(STEEL_BAR, 0.008)
            )
    return parts


def draw_house(scene: Scene, iso: Iso, *, margin: float = 0.45) -> House:
    ground = _top(
        scene, iso, -margin, LX + margin, -margin, LY + margin, 0, PAPER_DEEP
    ).stroke(RULE, 0.01)
    footing = _ring(
        scene,
        iso,
        (-0.15, LX + 0.15, -0.15, LY + 0.15),
        (0.3, LX - 0.3, 0.3, LY - 0.3),
        0,
        Z_FOUND,
    )
    plinth = _ring(scene, iso, (0, LX, 0, LY), (T, LX - T, T, LY - T), Z_FOUND, Z_BASE)

    steel: list[Drawable] = []
    masonry: list[Drawable] = []
    tops: list[Drawable] = []
    concrete: list[Drawable] = []
    layers: list[tuple[Drawable, float]] = []
    for k in range(COURSES):
        z0, z1 = _course_z(k)
        k_steel: list[Drawable] = []
        k_masonry: list[Drawable] = []
        k_tops: list[Drawable] = []
        k_concrete: list[Drawable] = []
        for element in ELEMENTS:
            if isinstance(element, Column):
                k_steel += _steel(scene, iso, element, z0, z1)
                k_concrete += _column_course(scene, iso, element, k)
            elif isinstance(element, Lintel):
                if LINTEL <= k < ABOVE:
                    color = CONCRETE_FRONT if element.axis == "y" else CONCRETE_SIDE
                    k_masonry.append(
                        _face(
                            scene,
                            iso,
                            element.axis,
                            element.plane,
                            element.a0,
                            element.a1,
                            z0,
                            z1,
                            color,
                        )
                    )
            elif element.courses[0] <= k < element.courses[1]:
                parts, top = _panel_course(scene, iso, element, k)
                k_masonry += parts
                # La cara superior se queda si el paño termina bajo el techo (alféizar).
                if k == element.courses[1] - 1 < COURSES - 1:
                    k_masonry.append(top)
                else:
                    k_tops.append(top)
        groups = [
            scene.geometry.group(k_steel),
            scene.geometry.group(k_masonry),
            scene.geometry.group(k_concrete),
            scene.geometry.group(k_tops),
        ]
        steel.append(groups[0])
        masonry.append(groups[1])
        concrete.append(groups[2])
        tops.append(groups[3])
        # El acero queda oculto tras el concreto antes del sismo y no se desplaza.
        share = (k + 0.5) / COURSES
        layers += [(g, share) for g in groups[1:]]

    # Remate del acero sobre la última hilada: queda dentro de la viga.
    crown = scene.geometry.group(
        [
            part
            for element in ELEMENTS
            if isinstance(element, Column)
            for part in _steel(scene, iso, element, Z_TOP, Z_ROOF - 0.03)
        ]
    )
    steel.append(crown)

    beams = [
        _face(scene, iso, "y", LY - T, T, LX - T, Z_TOP, Z_ROOF, CONCRETE_FRONT),
        _face(scene, iso, "x", T, T, LY - T, Z_TOP, Z_ROOF, CONCRETE_SIDE),
        _top(scene, iso, 0, LX, LY - T, LY, Z_ROOF, CONCRETE_TOP),
        _top(scene, iso, 0, T, 0, LY, Z_ROOF, CONCRETE_TOP),
        _top(scene, iso, LX - T, LX, 0, LY, Z_ROOF, CONCRETE_TOP),
        _top(scene, iso, 0, LX, 0, T, Z_ROOF, CONCRETE_TOP),
        _face(scene, iso, "y", 0, 0, LX, Z_TOP, Z_ROOF, CONCRETE_FRONT),
        _face(scene, iso, "x", LX, 0, LY, Z_TOP, Z_ROOF, CONCRETE_SIDE),
    ]
    slab_mask = _top(scene, iso, T, LX - T, T, LY - T, Z_ROOF, CONCRETE_TOP).opacity(0)
    slab = scene.geometry.fill_level(
        slab_mask, CONCRETE_TOP, 0, direction="right", keep_outline=False
    )
    layers += [*[(b, 1.0) for b in beams], (slab_mask, 1.0), (slab, 1.0)]
    return House(
        iso,
        ground,
        footing,
        plinth,
        steel,
        masonry,
        tops,
        concrete,
        beams,
        slab,
        slab_mask,
        layers,
    )
