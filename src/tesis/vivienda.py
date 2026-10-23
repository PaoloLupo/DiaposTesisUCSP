"""Vivienda de albañilería confinada en el mundo 3D, hilada por hilada.

Modelo en metros: x a lo largo de la fachada, y en profundidad, z hacia arriba
(``tesis.model3d`` lo lleva al mundo de Gaanim). Cada hilada es un grupo con sus
ladrillos, el mortero de sus juntas, el concreto de las columnas y los dinteles: los
ladrillos de una hilada son un solo objeto de copias (``instances``) que se asientan
uno tras otro, y el sismo desplaza cada hilada según su altura, así que la vivienda
se deforma por corte como una unidad.

Los extremos dentados de los paños entran en el hueco de las columnas: se ven
mientras solo está el acero y quedan dentro del concreto cuando se vacía.
"""

import random
from dataclasses import dataclass, field
from typing import Literal

from gaanim import (
    Anim,
    Color,
    Composition,
    Drawable,
    Easing,
    EasingCurve,
    Material3D,
    Parameter,
    Scene,
    sequence,
)

from tesis.model3d import P3, carry, lay_flat
from tesis.theme import BRICK, PAPER_DEEP, RULE

LX, LY = 6.0, 4.2  # planta, m
T = 0.15  # espesor del muro de soga
COL = 0.25  # lado de la columna a lo largo del muro
DOOR = (3.6, 4.5)  # vano de la puerta en la fachada
WINDOW = (1.5, 2.7)  # vano de la ventana en el muro derecho
Z_FOUND = 0.2  # cimiento corrido
Z_BASE = 0.4  # sobrecimiento: arranque del muro
Z_TOP = 2.8  # última hilada
Z_ROOF = 3.0  # viga solera y losa
SLAB = 0.12  # espesor de la losa
COURSES = 23
COURSE = (Z_TOP - Z_BASE) / COURSES
# Vanos por hiladas: alféizar 0–8, ventana 9–18, puerta 0–18, dintel 19–20 y
# dos hiladas de muro sobre el dintel.
SILL, LINTEL, ABOVE = 9, 19, 21
BRICK_PITCH = 0.25  # ladrillo con junta
JOINT = 0.014
TOOTH = 0.08  # dentado, exagerado para que se lea a esta escala
INSET = 0.045  # recubrimiento del acero
RECESS = 0.012  # el mortero queda hundido respecto de la cara del ladrillo
PROUD = 0.006  # el concreto de las columnas cubre la cara de los ladrillos dentados

MORTAR = Color.from_hex("#D8CDBF")
CONCRETE = Color.from_hex("#D9D7D2")
STEEL_BAR = Color.from_hex("#4E535C")
# Tonos de ladrillo: el mismo color con leves variaciones de horno.
BRICK_TONES = [Color.from_hex(c) for c in ("#B8532F", "#B04E2C", "#C05A34", "#A94A29")]
SINE = Easing.ease_in_out(EasingCurve.SINE)

ALL = (0, COURSES)


def toothed(course: int) -> bool:
    """En hiladas alternas el ladrillo extremo entra en la columna."""
    return course % 2 == 0


@dataclass(frozen=True)
class Column:
    x0: float
    x1: float
    y0: float
    y1: float

    @property
    def bars(self) -> list[tuple[float, float]]:
        return [
            (x, y)
            for x in (self.x0 + INSET, self.x1 - INSET)
            for y in (self.y0 + INSET, self.y1 - INSET)
        ]


@dataclass(frozen=True)
class Panel:
    """Paño de ladrillo entre dos columnas: ``fixed`` es la cara exterior del muro."""

    direction: Literal["X", "Y"]
    fixed: float
    inner: float  # cara interior
    start: float
    end: float
    teeth: tuple[bool, bool] = (False, False)  # dentado al inicio y al final
    courses: tuple[int, int] = ALL


@dataclass(frozen=True)
class Lintel:
    """Dintel de concreto sobre un vano."""

    direction: Literal["X", "Y"]
    fixed: float
    inner: float
    start: float
    end: float


COLUMNS = (
    Column(0, COL, LY - COL, LY),
    Column(LX - COL, LX, LY - COL, LY),
    Column(0, COL, 0, COL),
    Column(LX - T, LX, WINDOW[1], WINDOW[1] + COL),
    Column(LX - T, LX, WINDOW[0] - COL, WINDOW[0]),
    Column(DOOR[0] - COL, DOOR[0], 0, T),
    Column(DOOR[1], DOOR[1] + COL, 0, T),
    Column(LX - COL, LX, 0, COL),
)
# Paños en el orden en que se asienta cada hilada: fondo, izquierda, derecha y fachada.
PANELS = (
    Panel("X", LY, LY - T, COL, LX - COL),
    Panel("Y", 0, T, COL, LY - COL),
    Panel("Y", LX, LX - T, WINDOW[1] + COL, LY - COL, (True, True)),
    Panel("Y", LX, LX - T, *WINDOW, courses=(0, SILL)),  # alféizar
    Panel("Y", LX, LX - T, *WINDOW, courses=(ABOVE, COURSES)),
    Panel("Y", LX, LX - T, COL, WINDOW[0] - COL, (True, True)),
    Panel("X", 0, T, COL, DOOR[0] - COL, (True, True)),
    Panel("X", 0, T, *DOOR, courses=(ABOVE, COURSES)),
    Panel("X", 0, T, DOOR[1] + COL, LX - COL, (True, True)),
)
LINTELS = (Lintel("Y", LX, LX - T, *WINDOW), Lintel("X", 0, T, *DOOR))


@dataclass
class House:
    ground: Drawable
    footing: list[Drawable]  # cimiento corrido
    plinth: list[Drawable]  # sobrecimiento
    steel: list[Drawable]  # barras y estribos de cada columna
    bricks: list[Drawable]  # ladrillos y dinteles de cada hilada (copias de un cubo)
    mortar: list[Drawable]  # juntas de cada hilada
    concrete: list[Drawable]  # columnas, un objeto por hilada
    beams: list[Drawable]
    slab: Drawable
    drift: Parameter  # cuánto de la deriva se aplica: 1 en el primer vaivén
    # Grupos que se desplazan juntos en el sismo, con su fracción de la deriva.
    layers: list[tuple[Drawable, float]] = field(default_factory=list)

    def pour_slab(self, duration: float) -> list[Anim]:
        """La losa se vacía de izquierda a derecha, de una viga a la otra."""
        x0, x1 = T, LX - T
        return [
            self.slab.animate.scale_to_3d(x1 - x0, LY - 2 * T, SLAB)
            .duration(duration)
            .easing(Easing.LINEAR),
            self.slab.animate.move_to_3d((x0 + x1) / 2, LY / 2, Z_ROOF - SLAB / 2)
            .duration(duration)
            .easing(Easing.LINEAR),
        ]

    def sway(self, dx: float, dy: float) -> Composition:
        """Vaivén amortiguado: cada hilada se desplaza en proporción a su altura.

        Cada grupo se deforma desde el cursor con un desplazamiento uniforme, su
        fracción de ``(dx, dy)``, y el vaivén anima cuánto se aplica.
        """
        for layer, share in self.layers:
            carry(layer, (share * dx, share * dy, 0.0), self.drift)
        return sequence(
            *[
                self.drift.animate.set(amplitude).duration(0.36).easing(SINE)
                for amplitude in (1.0, -0.75, 0.5, -0.3, 0.12, 0.0)
            ]
        )


def _box(
    x0: float, x1: float, y0: float, y1: float, z0: float, z1: float
) -> tuple[P3, P3]:
    """Centro y escala de una caja del modelo, para una copia de un cubo."""
    center = (x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2
    return center, (x1 - x0, y1 - y0, z1 - z0)


def _solid(scene: Scene, box: tuple[P3, P3], color: Color) -> Drawable:
    center, (sx, sy, sz) = box
    return (
        scene.geometry.cube(1.0, material=Material3D.matte(color))
        .scale_to_3d(sx, sy, sz)
        .move_to_3d(*center)
        .hidden()
    )


def _copies(
    scene: Scene,
    boxes: list[tuple[P3, P3]],
    color: Color,
    colors: list[Color] | None = None,
) -> Drawable:
    """Un objeto de copias de un cubo: una caja por elemento, en el orden de la lista."""
    template = scene.geometry.cube(1.0, material=Material3D.matte(color))
    return scene.geometry.instances(
        template,
        [center for center, _ in boxes],
        scales=[scale for _, scale in boxes],
        colors=colors,
    ).hidden()


def _span(
    direction: str,
    fixed: float,
    inner: float,
    a: float,
    b: float,
    z0: float,
    z1: float,
    inset: float = 0.0,
) -> tuple[P3, P3]:
    lo, hi = sorted((fixed, inner))
    lo, hi = lo + inset, hi - inset
    if direction == "X":
        return _box(a, b, lo, hi, z0, z1)
    return _box(lo, hi, a, b, z0, z1)


def _course(
    k: int, rng: random.Random
) -> tuple[list[tuple[P3, P3]], list[Color], list[tuple[P3, P3]]]:
    """Ladrillos y dinteles (con su color) y juntas de la hilada ``k``."""
    z0 = Z_BASE + k * COURSE
    z1 = z0 + COURSE
    bricks: list[tuple[P3, P3]] = []
    tones: list[Color] = []
    joints: list[tuple[P3, P3]] = []
    for panel in PANELS:
        if not panel.courses[0] <= k < panel.courses[1]:
            continue
        s0 = panel.start - (TOOTH if panel.teeth[0] and toothed(k) else 0)
        s1 = panel.end + (TOOTH if panel.teeth[1] and toothed(k) else 0)
        joints.append(
            _span(panel.direction, panel.fixed, panel.inner, s0, s1, z0, z1, RECESS)
        )
        s = s0 - (BRICK_PITCH / 2 if k % 2 else 0)
        while s < s1 - 0.02:
            a, b = max(s, s0), min(s + BRICK_PITCH, s1)
            if b - a > 0.05:
                bricks.append(
                    _span(
                        panel.direction,
                        panel.fixed,
                        panel.inner,
                        a + JOINT / 2,
                        b - JOINT / 2,
                        z0 + JOINT / 2,
                        z1 - JOINT / 2,
                    )
                )
                tones.append(rng.choice(BRICK_TONES))
            s += BRICK_PITCH
    if LINTEL <= k < ABOVE:
        # Los dinteles se asientan con su hilada, sobre el vano y en concreto.
        for lt in LINTELS:
            bricks.append(
                _span(
                    lt.direction,
                    lt.fixed,
                    lt.inner,
                    lt.start - COL,
                    lt.end + COL,
                    z0,
                    z1,
                )
            )
            tones.append(CONCRETE)
    return bricks, tones, joints


def _ring(
    scene: Scene,
    outer: tuple[float, float, float, float],
    inner: tuple[float, float, float, float],
    z0: float,
    z1: float,
) -> list[Drawable]:
    """Anillo de concreto (cimiento, sobrecimiento o viga solera) en cuatro tramos."""
    x0, x1, y0, y1 = outer
    i0, i1, j0, j1 = inner
    boxes = [
        _box(x0, x1, y0, j0, z0, z1),
        _box(x0, x1, j1, y1, z0, z1),
        _box(x0, i0, j0, j1, z0, z1),
        _box(i1, x1, j0, j1, z0, z1),
    ]
    return [_solid(scene, box, CONCRETE) for box in boxes]


def _steel(scene: Scene, column: Column) -> list[Drawable]:
    """Cuatro barras ancladas en el cimiento y los estribos como una sola línea.

    Los tramos que unen un estribo con el siguiente corren sobre una barra, así que
    una polilínea dibuja todos los estribos de la columna.
    """
    top = Z_ROOF - 0.03
    parts = [
        scene.geometry.polyline_3d([(x, y, 0.05), (x, y, top)])
        .stroke(STEEL_BAR, 0.014)
        .hidden()
        for x, y in column.bars
    ]
    a0, a1 = column.x0 + INSET, column.x1 - INSET
    b0, b1 = column.y0 + INSET, column.y1 - INSET
    rings: list[P3] = []
    for i in range(12):
        z = Z_BASE + 0.1 + 0.2 * i
        rings += [
            (a0, b0, z),
            (a1, b0, z),
            (a1, b1, z),
            (a0, b1, z),
            (a0, b0, z),
        ]
    parts.append(scene.geometry.polyline_3d(rings).stroke(STEEL_BAR, 0.009).hidden())
    return parts


def build_house(scene: Scene, *, margin: float = 0.45) -> House:
    """Crea toda la vivienda oculta; la diapositiva decide cuándo aparece cada parte."""
    ground = lay_flat(
        scene.geometry.group(
            [
                scene.geometry.polygon(
                    [
                        (-margin, -margin),
                        (LX + margin, -margin),
                        (LX + margin, LY + margin),
                        (-margin, LY + margin),
                    ]
                )
                .fill(PAPER_DEEP)
                .stroke(RULE, 0.015)
            ],
            origin=(0, 0),
        ).hidden(),
        -0.005,
    )
    footing = _ring(
        scene,
        (-0.15, LX + 0.15, -0.15, LY + 0.15),
        (0.3, LX - 0.3, 0.3, LY - 0.3),
        0,
        Z_FOUND,
    )
    plinth = _ring(scene, (0, LX, 0, LY), (T, LX - T, T, LY - T), Z_FOUND, Z_BASE)
    steel = [part for column in COLUMNS for part in _steel(scene, column)]

    rng = random.Random(7)
    bricks: list[Drawable] = []
    mortar: list[Drawable] = []
    concrete: list[Drawable] = []
    layers: list[tuple[Drawable, float]] = []
    for k in range(COURSES):
        z0 = Z_BASE + k * COURSE
        k_bricks, tones, k_joints = _course(k, rng)
        bricks.append(_copies(scene, k_bricks, BRICK, tones))
        mortar.append(_copies(scene, k_joints, MORTAR))
        # La columna sobresale apenas de la cara del muro: el dentado queda adentro.
        concrete.append(
            _copies(
                scene,
                [
                    _box(
                        c.x0 - PROUD,
                        c.x1 + PROUD,
                        c.y0 - PROUD,
                        c.y1 + PROUD,
                        z0,
                        z0 + COURSE,
                    )
                    for c in COLUMNS
                ],
                CONCRETE,
            )
        )
        course = scene.geometry.group([bricks[-1], mortar[-1], concrete[-1]])
        layers.append((course, (k + 0.5) / COURSES))

    beams = _ring(scene, (0, LX, 0, LY), (T, LX - T, T, LY - T), Z_TOP, Z_ROOF)
    # La losa empieza como una lámina sobre la viga izquierda y se vacía hacia la derecha.
    slab = _solid(scene, _box(T, T + 0.001, T, LY - T, Z_ROOF - SLAB, Z_ROOF), CONCRETE)
    layers += [(b, 1.0) for b in beams]
    layers.append((slab, 1.0))
    drift = scene.viz.parameter(0.0)
    return House(
        ground,
        footing,
        plinth,
        steel,
        bricks,
        mortar,
        concrete,
        beams,
        slab,
        drift,
        layers,
    )


def ground_arrow(
    scene: Scene, start: tuple[float, float], end: tuple[float, float], color: Color
) -> Drawable:
    """Vector dibujado sobre el terreno, en coordenadas de planta (m).

    Devuelve la flecha, oculta: crece con ``grow_arrow`` dentro de su grupo tendido.
    """
    arrow = (
        scene.geometry.arrow(
            *start, *end, head_length=0.32, head_width=0.32, body_width=0.08
        )
        .fill(color)
        .no_stroke()
        .hidden()
    )
    lay_flat(scene.geometry.group([arrow], origin=(0, 0)), 0.01)
    return arrow


def mid(p: tuple[float, float], q: tuple[float, float]) -> P3:
    return (p[0] + q[0]) / 2, (p[1] + q[1]) / 2, 0.0
