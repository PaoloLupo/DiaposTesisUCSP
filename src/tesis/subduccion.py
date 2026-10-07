"""Bloque diagrama de la subducción de Nazca bajo la Sudamericana, en axonometría.

Sustituye a la animación Lottie: el mismo bloque (corte con la losa que se hunde,
superficie del mar y del continente) dibujado con polígonos planos, así que comparte
el estilo del deck y no carga un archivo de 7 MB al abrir la presentación.

Modelo en unidades libres: y a lo largo de la convergencia (0 en el océano, L en el
continente), x en profundidad (x = D es la cara del corte) y z hacia arriba. La vista
deja ver el corte, el extremo oceánico (y = 0) y la superficie. Sombreado plano:
superficie clara, corte medio y extremo oscuro.
"""

import math
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING

from gaanim import (
    Color,
    Drawable,
    Easing,
    EasingCurve,
    Playable,
    Scene,
    StrokeStyle,
    parallel,
    sequence,
    stagger,
)

from tesis.theme import CARD, FAIL, INK_SOFT, STEEL

if TYPE_CHECKING:  # `gaanim` no reexporta el tipo; basta para las anotaciones
    from gaanim.gaanim_core import Axonometric

L, D, H = 10.0, 6.0, 3.0  # largo, fondo y alto del bloque
SEA = 2.75  # superficie del mar
FLOOR = 2.5  # fondo marino: techo de la placa de Nazca
LAND = H  # superficie del continente
TRENCH = 4.4  # la losa empieza a doblarse en la fosa
COAST = 5.1  # el talud continental llega al nivel del mar
SHORE = 5.5  # y a la superficie del continente
SLAB = 0.55  # espesor de la placa oceánica
CRUST = 1.0  # espesor de la corteza continental
BEND = 2.6  # radio del codo de la losa; mayor que la banda más honda del manto
DIP = math.radians(42)  # buzamiento de la losa después del codo
BAND = 0.4  # bandas del manto bajo la losa
WEDGE = (1.5, 0.8)  # bandas horizontales del manto bajo el continente
QUAKE_Y = 5.5  # hipocentro sobre el contacto, bajo la costa
# Anchos de trazo en unidades del modelo: se escalan con el bloque.
SEAM = 0.03  # mismo color que la cara: tapa las costuras entre caras vecinas
EDGE = 0.04  # contorno de las flechas
LINE = 0.07  # anillos del sismo y marcas de la losa

# Vista del Lottie original: el largo sube ~14° y el fondo baja ~38° en pantalla.
AZIMUTH = math.radians(60.3)
ELEVATION = math.radians(26.6)

SEA_TOP = Color.from_hex("#B7C9DB")
SHORE_TOP = Color.from_hex("#D6C7A6")
LAND_TOP = Color.from_hex("#E6DFCF")
WATER = (Color.from_hex("#9DB5CC"), Color.from_hex("#86A0BA"))  # corte, extremo
SLAB_FILL = (STEEL, Color.from_hex("#244A70"))
CRUST_FILL = Color.from_hex("#7B3B22")
MANTLE = (  # de la banda junto a la losa a la más profunda: (corte, extremo)
    (Color.from_hex("#A54A2B"), Color.from_hex("#8F3F24")),
    (Color.from_hex("#BC6542"), Color.from_hex("#A6573A")),
    (Color.from_hex("#CE845F"), Color.from_hex("#B8724F")),
    (Color.from_hex("#DEA484"), Color.from_hex("#C98F70")),
    (Color.from_hex("#EBC3AC"), Color.from_hex("#D9AE96")),
)

type Point2 = tuple[float, float]
type Profile = list[Point2]
type Point3 = tuple[float, float, float]


_ELBOW = (TRENCH + BEND * math.sin(DIP), FLOOR - BEND * (1 - math.cos(DIP)))


def slab_top(y: float) -> float:
    """Techo de la placa de Nazca: plano, un codo circular en la fosa y una recta."""
    if y <= TRENCH:
        return FLOOR
    if y <= _ELBOW[0]:
        return FLOOR - BEND + math.sqrt(BEND**2 - (y - TRENCH) ** 2)
    return _ELBOW[1] - math.tan(DIP) * (y - _ELBOW[0])


def _slope(y: float) -> float:
    if y <= TRENCH:
        return 0.0
    if y <= _ELBOW[0]:
        return -math.tan(math.asin((y - TRENCH) / BEND))
    return -math.tan(DIP)


def slab_y(z: float) -> float:
    """Dónde el techo de la losa, ya bajo la fosa, pasa por la cota ``z``."""
    lo, hi = TRENCH, L + 3.0
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if slab_top(mid) > z else (lo, mid)
    return (lo + hi) / 2


EXIT = slab_y(0.0)  # la losa sale por el fondo del bloque
QUAKE = (QUAKE_Y, slab_top(QUAKE_Y) - 0.07)  # hipocentro, en el corte (y, z)


def _below_slab(depth: float, ys: Sequence[float]) -> Profile:
    """La curva paralela al techo de la losa, ``depth`` por debajo (en su normal)."""
    out: Profile = []
    for y in ys:
        slope = _slope(y)
        norm = math.hypot(slope, 1.0)
        out.append((y + depth * slope / norm, slab_top(y) - depth / norm))
    return out


def _span(start: float, stop: float, step: float = 0.1) -> list[float]:
    n = max(1, round(abs(stop - start) / step))
    return [start + (stop - start) * i / n for i in range(n + 1)]


def _cross(a: Point2, b: Point2, axis: int, value: float) -> Point2:
    t = (value - a[axis]) / (b[axis] - a[axis])
    return a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])


def _clip(poly: Profile) -> Profile:
    """Recorta un polígono del corte al rectángulo del bloque (Sutherland-Hodgman)."""
    sides: tuple[tuple[int, float, Callable[[float, float], bool]], ...] = (
        (0, 0.0, lambda v, lim: v >= lim),
        (0, L, lambda v, lim: v <= lim),
        (1, 0.0, lambda v, lim: v >= lim),
        (1, H, lambda v, lim: v <= lim),
    )
    for axis, limit, keep in sides:
        out: Profile = []
        for i, b in enumerate(poly):
            a = poly[i - 1]
            if keep(b[axis], limit):
                if not keep(a[axis], limit):
                    out.append(_cross(a, b, axis, limit))
                out.append(b)
            elif keep(a[axis], limit):
                out.append(_cross(a, b, axis, limit))
        poly = out
    return poly


def _above(curve: Profile) -> Profile:
    """Todo lo que queda sobre ``curve``, antes de recortar al bloque."""
    return [*curve, (L + 3.0, H + 1.0), (-2.0, H + 1.0)]


def _cut_regions() -> list[tuple[Profile, Color]]:
    """Regiones del corte en orden de dibujo, cada una ya recortada al bloque."""
    wide = _span(-2.0, L + 3.0)
    regions: list[tuple[Profile, Color]] = [
        ([(0, 0), (L, 0), (L, H), (0, H)], MANTLE[-1][0])
    ]
    # Bandas del manto paralelas a la losa, de la más profunda a la más cercana.
    for k in range(len(MANTLE) - 1, 0, -1):
        regions.append((_above(_below_slab(SLAB + k * BAND, wide)), MANTLE[k - 1][0]))
    # Bajo el continente, sobre la losa: bandas horizontales del manto.
    for level, (front, _) in zip(WEDGE, MANTLE[1:]):
        start = slab_y(level)
        wedge = [(y, slab_top(y)) for y in _span(start, L + 3.0)]
        regions.append(([(start, level), *wedge, (L + 3.0, level)], front))
    top = [(y, slab_top(y)) for y in wide]
    regions.append(([*top, *reversed(_below_slab(SLAB, wide))], SLAB_FILL[0]))
    base = LAND - CRUST
    contact = [(y, slab_top(y)) for y in _span(slab_y(base), TRENCH)]
    crust = [
        (TRENCH, FLOOR),
        (COAST, SEA),
        (SHORE, LAND),
        (L, LAND),
        (L, base),
        *contact,
    ]
    regions.append((crust, CRUST_FILL))
    regions.append(([(0, FLOOR), (TRENCH, FLOOR), (COAST, SEA), (0, SEA)], WATER[0]))
    return [(_clip(poly), color) for poly, color in regions]


def _end_bands() -> list[tuple[float, float, Color]]:
    """Capas del extremo oceánico (y = 0): (z inferior, z superior, color)."""
    bands = [(FLOOR, SEA, WATER[1]), (FLOOR - SLAB, FLOOR, SLAB_FILL[1])]
    z = FLOOR - SLAB
    for _, side in MANTLE[:-1]:
        bands.append((z - BAND, z, side))
        z -= BAND
    bands.append((0.0, z, MANTLE[-1][1]))
    return bands


def _flat_arrow(
    iso: Axonometric, x: float, y: float, z: float, length: float, sign: int
) -> Drawable:
    """Flecha acostada sobre una superficie, a lo largo de y (``sign`` = ±1)."""
    shaft, head, tip = 0.09, 0.24, 0.42
    y1, y2 = y + sign * (length - tip), y + sign * length
    pts: list[Point3] = [
        (x - shaft, y, z),
        (x - shaft, y1, z),
        (x - head, y1, z),
        (x, y2, z),
        (x + head, y1, z),
        (x + shaft, y1, z),
        (x + shaft, y, z),
    ]
    return iso.polygon(pts).fill(CARD).stroke(INK_SOFT, EDGE * iso.scale)


def _ring(radius: float) -> list[Point3]:
    """Círculo en el plano del corte alrededor del hipocentro."""
    qy, qz = QUAKE
    return [
        (D, qy + radius * math.cos(a), qz + radius * math.sin(a))
        for a in (2 * math.pi * i / 48 for i in range(48))
    ]


@dataclass
class SubductionBlock:
    """El bloque dibujado: ``root`` agrupa todo; los rótulos van en escena."""

    root: Drawable
    nazca: Point2  # sobre el mar, para el rótulo NAZCA
    south_america: Point2  # sobre el continente
    iso: Axonometric
    arrows: list[tuple[Drawable, int]]
    flow: Drawable
    rings: list[Drawable]
    focus: Drawable

    def motion(self, duration: float = 4.0) -> Playable:
        """Las placas convergen, la losa se hunde y el contacto libera un sismo."""
        ox, oy = self.iso.point(0, 0, 0)
        ex, ey = self.iso.point(0, 0.6, 0)
        drift = [
            arrow.animate.shift_by((ex - ox) * sign, (ey - oy) * sign)
            .duration(duration * 0.75)
            .easing(Easing.LINEAR)
            for arrow, sign in self.arrows
        ]
        sink = (
            self.flow.animate.dash_offset(-2.0 * self.iso.scale)
            .duration(duration * 0.75)
            .easing(Easing.LINEAR)
        )
        # Cada onda crece desde el hipocentro y se apaga en su segunda mitad; el
        # sismo cierra la animación, que dura ``duration`` como el Lottie que reemplaza.
        wave = [self.iso.point(*p) for p in _ring(1.6)]
        flash, grow, each, fade = 0.12, 1.25, 0.3, 0.3
        span = flash + each * (len(self.rings) - 1) + grow + fade
        quake = sequence(
            self.focus.animate.opacity(1).duration(flash),
            stagger(
                *[
                    sequence(
                        ring.animate.opacity(1).duration(0.05),
                        parallel(
                            ring.animate.points(wave)
                            .duration(grow - 0.05)
                            .easing(Easing.ease_out(EasingCurve.CUBIC)),
                            ring.animate.opacity(0).duration(0.6).delay(0.6),
                        ),
                    )
                    for ring in self.rings
                ],
                each=each,
            ),
            self.focus.animate.opacity(0).duration(fade),
        ).delay(max(0.0, duration - span))
        return parallel(*drift, sink, quake)


def draw_subduction(
    scene: Scene, center: Point2, width: float, *, z_index: int = 0
) -> SubductionBlock:
    """Dibuja el bloque con ``width`` unidades de escena de ancho, centrado en ``center``.

    Sus partes ocupan ``z_index`` en adelante (unas 30), de atrás hacia adelante.
    """
    unit = scene.geometry.axonometric(azimuth=AZIMUTH, elevation=ELEVATION)
    corners = [unit.point(x, y, z) for x in (0, D) for y in (0, L) for z in (0, H)]
    xs, ys = [p[0] for p in corners], [p[1] for p in corners]
    scale = width / (max(xs) - min(xs))
    mid = ((max(xs) + min(xs)) / 2 * scale, (max(ys) + min(ys)) / 2 * scale)
    iso = scene.geometry.axonometric(
        azimuth=AZIMUTH,
        elevation=ELEVATION,
        origin=(center[0] - mid[0], center[1] - mid[1]),
        scale=scale,
    )
    parts: list[Drawable] = []

    def face(points: Sequence[Point3], color: Color) -> None:
        parts.append(iso.polygon(points).fill(color).stroke(color, SEAM * scale))

    for poly, color in _cut_regions():
        if len(poly) >= 3:
            face([(D, y, z) for y, z in poly], color)
    for z0, z1, color in _end_bands():
        face([(0, 0, z0), (D, 0, z0), (D, 0, z1), (0, 0, z1)], color)
    for y0, z0, y1, z1, color in (
        (0.0, SEA, COAST, SEA, SEA_TOP),
        (COAST, SEA, SHORE, LAND, SHORE_TOP),
        (SHORE, LAND, L, LAND, LAND_TOP),
    ):
        face([(0, y0, z0), (D, y0, z0), (D, y1, z1), (0, y1, z1)], color)

    arrows = [
        (_flat_arrow(iso, 1.8, 0.7, SEA, 1.5, 1), 1),
        (_flat_arrow(iso, 4.3, 1.9, SEA, 1.5, 1), 1),
        (_flat_arrow(iso, 1.6, 9.2, LAND, 1.2, -1), -1),
        (_flat_arrow(iso, 4.1, 8.5, LAND, 1.2, -1), -1),
    ]
    # Marcas que bajan por el centro de la losa, en el corte.
    middle = _below_slab(SLAB / 2, _span(0.4, EXIT - 0.3))
    flow = (
        iso.polyline([(D, y, z) for y, z in middle if z > 0.12])
        .no_fill()
        .stroke_style(
            StrokeStyle(CARD, LINE * scale, dashes=[0.2 * scale, 0.35 * scale])
        )
    )
    focus = iso.polygon(_ring(0.09)).fill(FAIL).no_stroke().opacity(0)
    rings = [
        iso.polyline(_ring(0.06), closed=True)
        .no_fill()
        .stroke(FAIL, LINE * scale)
        .opacity(0)
        for _ in range(3)
    ]
    parts += [arrow for arrow, _ in arrows]
    parts += [flow, focus, *rings]
    for k, part in enumerate(parts):
        part.z_index(z_index + k)

    # Rótulos sobre el papel: NAZCA tras el borde del mar y SUDAMERICANA más allá
    # del extremo del continente, a la altura de su superficie.
    nx, ny = iso.point(0.0, 1.6, SEA)
    sx, sy = iso.point(1.6, L + 1.6, LAND)
    lift = 0.35 * scale
    return SubductionBlock(
        root=scene.geometry.group(parts),
        nazca=(nx, ny + lift),
        south_america=(sx, sy),
        iso=iso,
        arrows=arrows,
        flow=flow,
        rings=rings,
        focus=focus,
    )
