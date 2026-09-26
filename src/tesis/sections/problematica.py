"""Bloque 1 · Problemática: material, sistema sísmico y traslado manual de datos."""

import math

from gaanim import (
    Anchor,
    Color,
    Direction,
    Drawable,
    Easing,
    EasingCurve,
    Scene,
    Section,
    SectionStep,
    Transition,
    computed,
    parallel,
    sequence,
    stagger,
)

from tesis.data.materiales_inei import (
    MATERIALES_ORDENADOS,
    SOURCE_LABEL,
    TOTAL_VIVIENDAS,
)
from tesis.data.sudamerica import COUNTRIES, Ring
from tesis.data.sudamerica import SOURCE_LABEL as OUTLINES_SOURCE
from tesis.data.thesis import CRACKING_FLOOR1
from tesis.kit import (
    header,
    label,
    numeral,
    panel,
    pill,
    source,
    t,
    takeaway,
)
from tesis.theme import (
    BRICK,
    BRICK_DEEP,
    BRICK_SOFT,
    CARD,
    FAIL,
    DISPLAY,
    FAINT,
    INK,
    INK_SOFT,
    MONO,
    MUTED,
    PAPER,
    PAPER_DEEP,
    RULE,
    STEEL,
    STEEL_SOFT,
)
from tesis.vivienda import House, Iso, draw_house

KICKER = "01 · Problemática"
MATERIAL_LABELS = {
    "Ladrillo\no bloque": "Ladrillo o bloque de concreto",
    "Adobe": "Adobe",
    "Madera": "Madera",
    "Tapia": "Tapia",
    "Triplay\ncalamina\nestera": "Triplay, calamina o estera",
    "Quincha": "Quincha",
    "Piedra\nbarro": "Piedra con barro",
    "Piedra\nsillar": "Piedra o sillar",
    "Otro": "Otro material",
}


def materials(scene: Scene) -> None:
    header(scene, KICKER, "El ladrillo es el material usado en seis de cada diez viviendas")

    outline = (
        scene.media.svg("peru.svg")
        .no_fill()
        .stroke(INK_SOFT, 0.016)
        .scale_to(0.58)
        .move_to(-4.75, -0.15)
    )
    counter = scene.viz.rolling_number(
        0,
        decimals=1,
        suffix=" %",
        font_family=DISPLAY,
        weight=700,
        font_size=0.72,
        mode="continuous",
        color=INK,
    ).move_to(-4.55, -0.35, Anchor.CENTER)
    level = computed(lambda value: value / 100 - 0.1, inputs=[counter.parameter])
    fill = (
        scene.geometry.fill_level(
            outline, BRICK_SOFT, direction="up", keep_outline=False
        )
        .z_index(-1)
        .set_fill_level(level)
    )
    caption = t(
        scene,
        "de las viviendas del Perú tienen paredes\nde ladrillo o bloque de concreto",
        -4.75,
        -2.5,
        size=0.2,
        color=INK_SOFT,
        anchor=Anchor.TOP,
    )

    scene.play(outline.animate.create().duration(1.0))
    scene.play(
        [
            counter.visual.animate.fade_in().duration(0.3),
            caption.animate.fade_in().duration(0.5),
        ]
    )
    scene.play(
        counter.count_to(
            100 * MATERIALES_ORDENADOS[0][1] / TOTAL_VIVIENDAS, duration=1.6, snap=True
        )
    )
    scene.stop("material-predominante")

    # Barras horizontales: una sola serie destacada y el resto en gris cálido.
    label_x, bar_x, bar_max = 1.35, 1.55, 4.6
    top, gap = 2.2, 0.56
    scale = bar_max / 70
    title = label(
        scene,
        "Material predominante en paredes exteriores · % de viviendas",
        -1.0,
        2.62,
        color=MUTED,
        size=0.14,
    )
    rows: list[Drawable] = []
    bars: list[Drawable] = []
    for i, (name, count) in enumerate(MATERIALES_ORDENADOS):
        share = 100 * count / TOTAL_VIVIENDAS
        y = top - i * gap
        lead = i == 0
        rows.append(
            t(
                scene,
                MATERIAL_LABELS[name],
                label_x,
                y,
                size=0.22,
                weight=900 if lead else 400,
                color=INK if lead else INK_SOFT,
                anchor=Anchor.RIGHT,
            )
        )
        mask = (
            scene.geometry.rect(max(share * scale, 0.04), 0.3)
            .no_fill()
            .no_stroke()
            .move_to(bar_x + max(share * scale, 0.04) / 2, y)
        )
        bars.append(
            scene.geometry.fill_level(
                mask,
                BRICK if lead else "#CFC8BC",
                0,
                direction="right",
                keep_outline=False,
            )
        )
        rows.append(
            t(
                scene,
                f"{share:.1f} %",
                bar_x + share * scale + 0.14,
                y,
                font=MONO,
                size=0.19,
                color=BRICK_DEEP if lead else MUTED,
                anchor=Anchor.LEFT,
            )
        )
    scene.play(title.animate.fade_in().duration(0.4))
    scene.play(
        stagger(
            *[
                sequence(
                    rows[2 * i].animate.fade_in().duration(0.25),
                    bars[i].animate.fill_level(1).duration(0.5),
                    rows[2 * i + 1].animate.fade_in().duration(0.2),
                )
                for i in range(len(bars))
            ],
            each=0.09,
        )
    )
    source(
        scene,
        f"{SOURCE_LABEL} · Características de la vivienda (VIV6). "
        "El material de las paredes no acredita confinamiento ni desempeño sísmico.",
    )
    scene.stop("materiales-listo")


# Mapa de placas en Mercator, a todo el ancho útil. El alto del marco va de 1° N a
# 19° S y fija la escala; MAP_LON es la longitud que cae en x = 0, de modo que la
# fosa quede cerca del centro: Nazca a la izquierda, la Sudamericana a la derecha.
MAP_LEFT, MAP_RIGHT, MAP_TOP, MAP_BOTTOM = -7.3, 7.3, 2.73, -2.52
MAP_NORTH, MAP_SOUTH = 1.0, -19.0
MAP_LON = -80.8


def _merc(lat: float) -> float:
    """Ordenada de Mercator en grados, en la misma escala que la longitud."""
    return math.degrees(math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)))


MAP_K = (MAP_TOP - MAP_BOTTOM) / (_merc(MAP_NORTH) - _merc(MAP_SOUTH))


def _geo(lon: float, lat: float) -> tuple[float, float]:
    """Longitud y latitud a coordenadas de escena."""
    return (lon - MAP_LON) * MAP_K, MAP_TOP - (_merc(MAP_NORTH) - _merc(lat)) * MAP_K


# Traza aproximada de la fosa Perú-Chile (borde entre placas), de norte a sur.
TRENCH = [
    (-81.2, 1.0),
    (-81.5, -1.5),
    (-81.8, -3.5),
    (-82.0, -5.0),
    (-81.6, -7.0),
    (-80.6, -8.8),
    (-79.3, -10.7),
    (-78.2, -12.3),
    (-76.9, -14.0),
    (-75.6, -15.6),
    (-73.4, -17.1),
    (-71.6, -18.4),
    (-71.2, -19.0),
]

# Epicentros aproximados (USGS) de grandes sismos frente a la costa.
QUAKES = [
    ("Áncash", 1970, 7.9, -78.84, -9.25),
    ("Lima", 1940, 8.2, -77.80, -11.20),
    ("Pisco", 2007, 8.0, -76.60, -13.39),
    ("Arequipa", 2001, 8.4, -73.64, -16.26),
]
MW_RANGE = (7.9, 8.4)


def _intensity(mw: float) -> float:
    """Magnitud a [0, 1] dentro de los sismos mostrados (7.9 → 0, 8.4 → 1)."""
    low, high = MW_RANGE
    return (mw - low) / (high - low)


def _trench_teeth(
    scene: Scene, points: list[tuple[float, float]], step: float
) -> list[Drawable]:
    """Triángulos de subducción sobre la placa que cabalga, a intervalos regulares."""
    teeth: list[Drawable] = []
    carry = step / 2
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        seg = math.hypot(x1 - x0, y1 - y0)
        ux, uy = (x1 - x0) / seg, (y1 - y0) / seg
        nx, ny = (-uy, ux) if -uy > 0 else (uy, -ux)  # normal hacia el este
        d = carry
        while d < seg:
            bx, by = x0 + ux * d, y0 + uy * d
            half, tall = 0.055, 0.1
            teeth.append(
                scene.geometry.polygon(
                    [
                        (bx - ux * half, by - uy * half),
                        (bx + ux * half, by + uy * half),
                        (bx + nx * tall, by + ny * tall),
                    ]
                )
                .fill(INK)
                .no_stroke()
            )
            d += step
        carry = d - seg
    return teeth


def _outline(
    scene: Scene, rings: list[Ring], fill: Color, stroke: Color, width: float
) -> list[Drawable]:
    return [
        scene.geometry.polygon([_geo(lon, lat) for lon, lat in ring])
        .fill(fill)
        .stroke(stroke, width)
        for ring in rings
    ]


def _graticule(scene: Scene) -> tuple[list[Drawable], list[Drawable]]:
    """Paralelos y meridianos cada 5°, con rótulos en el borde izquierdo e inferior."""
    lines: list[Drawable] = []
    marks: list[Drawable] = []
    for lat in (0, -5, -10, -15):
        _, y = _geo(MAP_LON, lat)
        lines.append(
            scene.geometry.line(MAP_LEFT, y, MAP_RIGHT, y).stroke(MUTED, 0.008)
        )
        marks.append(
            t(
                scene,
                f"{-lat}° S" if lat else "0°",
                MAP_LEFT + 0.08,
                y + 0.03,
                font=MONO,
                size=0.11,
                color=MUTED,
                anchor=Anchor.BOTTOM_LEFT,
            )
        )
    for lon in range(-105, -50, 5):
        x, _ = _geo(lon, 0)
        if not MAP_LEFT < x < MAP_RIGHT:
            continue
        lines.append(
            scene.geometry.line(x, MAP_BOTTOM, x, MAP_TOP).stroke(MUTED, 0.008)
        )
        if lon % 10 == 0 and lon < -80:
            marks.append(
                t(
                    scene,
                    f"{-lon}° O",
                    x + 0.05,
                    MAP_BOTTOM + 0.05,
                    font=MONO,
                    size=0.11,
                    color=MUTED,
                    anchor=Anchor.BOTTOM_LEFT,
                )
            )
    return [line.opacity(0.3).z_index(-2) for line in lines], marks


def plates(scene: Scene) -> None:
    header(scene, KICKER, "El Perú está sobre el choque de dos placas tectónicas")

    # El Perú resalta sobre sus vecinos: ellos toman el tono de la placa (tierra y mar
    # son la misma placa Sudamericana) y se recortan al marco.
    frame = (
        scene.geometry.rect(MAP_RIGHT - MAP_LEFT, MAP_TOP - MAP_BOTTOM)
        .fill(CARD)
        .no_stroke()
        .opacity(0)
        .move_to(0, (MAP_TOP + MAP_BOTTOM) / 2)
    )
    peru = scene.geometry.group(_outline(scene, COUNTRIES["PER"], CARD, INK_SOFT, 0.014))
    neighbors = (
        scene.geometry.group(
            [
                shape
                for code, rings in COUNTRIES.items()
                if code != "PER"
                for shape in _outline(scene, rings, PAPER_DEEP, RULE, 0.012)
            ]
        )
        .z_index(-1)
        .clip(frame)
    )
    peru_name = label(
        scene, "Perú", *_geo(-74.4, -4.9), size=0.2, color=INK_SOFT, anchor=Anchor.CENTER
    )
    places = [
        label(scene, name, *_geo(lon, lat), size=0.12, color=MUTED, anchor=Anchor.CENTER)
        for name, lon, lat in (
            ("Ecuador", -78.4, -1.4),
            ("Colombia", -71.8, -0.6),
            ("Brasil", -58.0, -11.5),
            ("Bolivia", -64.6, -16.4),
        )
    ]
    places.append(
        t(
            scene,
            "Galápagos",
            *_geo(-91.9, -0.8),
            size=0.12,
            color=MUTED,
            anchor=Anchor.RIGHT,
        )
    )
    scene.play(
        [
            peru.animate.create().duration(1.0),
            peru_name.animate.fade_in().duration(0.5).delay(0.6),
        ]
    )

    # Dos placas: el Perú entero está sobre la Sudamericana; la fosa marca el contacto.
    trench = [_geo(lon, lat) for lon, lat in TRENCH]
    nazca = (
        scene.geometry.polygon([(MAP_LEFT, MAP_TOP), *trench, (MAP_LEFT, MAP_BOTTOM)])
        .fill(STEEL_SOFT)
        .no_stroke()
        .z_index(-3)
    )
    southam = (
        scene.geometry.polygon([*trench, (MAP_RIGHT, MAP_BOTTOM), (MAP_RIGHT, MAP_TOP)])
        .fill(PAPER_DEEP)
        .no_stroke()
        .z_index(-3)
    )
    grid, grid_marks = _graticule(scene)
    # Rótulos de placa en dos líneas y altos: quedan fuera de las vistas del recorrido.
    nazca_label = t(
        scene,
        "PLACA\nDE NAZCA",
        MAP_LEFT + 0.4,
        0.9,
        font=MONO,
        size=0.24,
        weight=700,
        color=STEEL,
        anchor=Anchor.LEFT,
    )
    southam_label = t(
        scene,
        "PLACA\nSUDAMERICANA",
        MAP_RIGHT - 0.4,
        0.9,
        font=MONO,
        size=0.24,
        weight=700,
        color=INK_SOFT,
        anchor=Anchor.RIGHT,
    )
    line = scene.geometry.polyline(trench).no_fill().stroke(INK, 0.025)
    teeth = _trench_teeth(scene, trench, 0.28)
    tx, ty = _geo(-82.4, -3.2)
    trench_label = t(
        scene,
        "Fosa Perú-Chile",
        tx - 0.12,
        ty,
        size=0.17,
        color=INK,
        weight=700,
        anchor=Anchor.RIGHT,
    )
    scene.play(
        stagger(
            parallel(
                nazca.animate.fade_in().duration(0.5),
                *[g.animate.fade_in().duration(0.5) for g in grid + grid_marks],
                nazca_label.animate.fade_in_from(Direction.RIGHT, 0.1).duration(0.5),
            ),
            parallel(
                southam.animate.fade_in().duration(0.5),
                neighbors.animate.fade_in().duration(0.5),
                *[p.animate.fade_in().duration(0.5) for p in places],
                southam_label.animate.fade_in_from(Direction.LEFT, 0.1).duration(0.5),
            ),
            each=0.35,
        )
    )
    scene.play(
        [
            line.animate.create().duration(0.9),
            stagger(
                *[p.animate.grow_from_center().duration(0.2) for p in teeth],
                each=0.9 / len(teeth),
            ),
            trench_label.animate.fade_in().duration(0.5),
        ]
    )

    # La placa de Nazca converge hacia el este-noreste, contra el continente.
    pushes: list[Drawable] = []
    for lat in (-9.5, -15.0):
        x1, y1 = _geo(-83.2, lat)
        pushes.append(
            scene.geometry.arrow(
                x1 - 1.2,
                y1 - 0.24,
                x1,
                y1,
                head_length=0.2,
                head_width=0.22,
                body_width=0.07,
            )
            .fill(STEEL)
            .no_stroke()
        )
    ax, ay = _geo(-83.2, -15.0)
    rate = t(
        scene,
        "≈ 7–8 cm/año",
        ax,
        ay - 0.3,
        font=MONO,
        size=0.16,
        color=STEEL,
        anchor=Anchor.TOP_RIGHT,
    )
    scene.play(
        [
            *[a.animate.grow_arrow().duration(0.6) for a in pushes],
            rate.animate.fade_in().duration(0.5),
        ]
    )
    scene.stop("dos-placas")

    # Paso temporal al mecanismo: la cámara entra en la fosa frente a Lima y el mapa
    # cede la pantalla al bloque en 3D. Lo que aparece encima se construye en
    # coordenadas de pantalla (divididas por el zoom) alrededor del centro de la vista.
    zoom = 3.0
    cx, cy = _geo(-78.4, -12.0)

    def at(sx: float, sy: float) -> tuple[float, float]:
        return cx + sx / zoom, cy + sy / zoom

    veil = (
        scene.geometry.rect(16 / zoom + 0.2, 9 / zoom + 0.2)
        .fill(PAPER)
        .no_stroke()
        .move_to(cx, cy)
        .z_index(30)
    )
    block_scale, block_y = 0.72, 0.35
    block = scene.media.lottie("placas_subduccion_paleta.lottie")
    block.scale_by(block_scale / zoom).move_to(*at(0, block_y)).z_index(31)
    block_labels = [
        t(
            scene,
            name,
            *at(dx * block_scale, block_y + dy * block_scale),
            font=MONO,
            size=0.2 / zoom,
            weight=700,
            color=color,
            anchor=Anchor.CENTER,
        ).z_index(31)
        for name, dx, dy, color in (
            ("NAZCA", -4.33, 2.25, STEEL),
            ("SUDAMERICANA", 4.52, 2.98, INK_SOFT),
        )
    ]
    explain = t(
        scene,
        "La placa de Nazca se hunde (subduce) bajo la Sudamericana.\n"
        "El contacto se traba, acumula energía y la libera en sismos.",
        *at(0, -2.75),
        size=0.26 / zoom,
        color=INK_SOFT,
        anchor=Anchor.TOP,
    ).z_index(31)
    scene.play(
        scene.camera.animate.to(scene.camera.state_2d((cx, cy), zoom))
        .duration(1.2)
        .easing(Easing.ease_in_out(EasingCurve.CUBIC))
    )
    scene.play(
        [
            veil.animate.fade_in().duration(0.6),
            sequence(block.animate.fade_in().duration(0.5), block).delay(0.3),
            *[b.animate.fade_in().duration(0.4).delay(0.8) for b in block_labels],
            explain.animate.fade_in().duration(0.6).delay(1.1),
        ]
    )
    scene.stop("subduccion")
    scene.play(
        [
            block.animate.fade_out().duration(0.5),
            *[b.animate.fade_out().duration(0.4) for b in block_labels],
            explain.animate.fade_out().duration(0.4),
            veil.animate.fade_out().duration(0.6).delay(0.3),
        ]
    )

    # Grandes sismos del último siglo: todos frente a la costa, sobre el contacto.
    marks = []
    for name, year, mw, lon, lat in QUAKES:
        x, y = _geo(lon, lat)
        dot = (
            scene.geometry.circle(0.07)
            .fill(FAIL)
            .no_stroke()
            .move_to(x, y)
            .z_index(5)
        )
        ring = (
            scene.geometry.circle(0.07)
            .no_fill()
            .stroke(FAIL, 0.02)
            .move_to(x, y)
            .z_index(5)
            .opacity(0)
        )
        # El nombre va encima y el dato a la altura del epicentro: la costa baja
        # hacia el sureste y, frente a Arequipa, la frontera con Bolivia queda a
        # 1.2 unidades del punto, así que ninguna línea cruza los rótulos.
        place = t(
            scene, name, x + 0.19, y + 0.2, size=0.17, weight=700, color=INK, anchor=Anchor.LEFT
        ).z_index(6)
        detail = t(
            scene,
            f"{year} · Mw {mw}",
            x + 0.19,
            y,
            font=MONO,
            size=0.115,
            color=INK_SOFT,
            anchor=Anchor.LEFT,
        ).z_index(6)
        marks.append(
            stagger(
                parallel(
                    dot.animate.grow_from_center().duration(0.25),
                    sequence(
                        ring.animate.fade_in().duration(0.05),
                        parallel(
                            # La onda crece más cuanto mayor es la magnitud.
                            ring.animate.scale_to(4 + 5 * _intensity(mw)).duration(0.8),
                            ring.animate.fade_out().duration(0.8),
                        ),
                    ),
                ),
                parallel(
                    place.animate.fade_in_from(Direction.LEFT, 0.08).duration(0.35),
                    detail.animate.fade_in_from(Direction.LEFT, 0.08).duration(0.35),
                ),
                each=0.15,
            )
        )
    # Desde la fosa, la cámara recorre la costa de norte a sur y sacude la escena en
    # cada evento con un trauma proporcional a la magnitud: Arequipa (8.4) sacude
    # visiblemente más que Áncash (7.9). El encuadre no sale del mapa y al final
    # vuelve a la vista completa.
    half_w, half_h = 8 / zoom, 4.5 / zoom
    tour = []
    shake_time = 0.8
    for i, (mark, (*_, mw, lon, lat)) in enumerate(zip(marks, QUAKES, strict=True)):
        x, y = _geo(lon, lat)
        view = (
            min(x + 1.1, MAP_RIGHT - half_w),
            min(max(y, MAP_BOTTOM + half_h), MAP_TOP - half_h),
        )
        tour.append(
            sequence(
                scene.camera.animate.to(scene.camera.state_2d(view, zoom))
                .duration(0.8)
                .easing(Easing.ease_in_out(EasingCurve.CUBIC)),
                parallel(mark, _quake_shake(scene, mw, shake_time, seed=i)),
                gap=-0.1,
            )
        )
    scene.play(sequence(*tour, gap=0.25))
    scene.play(
        scene.camera.animate.reset()
        .duration(1.1)
        .easing(Easing.ease_in_out(EasingCurve.CUBIC))
    )
    takeaway(
        scene,
        "Toda la costa está frente al borde de placas: el sismo es una certeza",
    )
    source(
        scene,
        "Tesis · §1.1 Problemática, p. 1 (Tavera, 2014). Fosa y epicentros aproximados "
        f"(USGS); contornos: {OUTLINES_SOURCE}; mapa esquemático.",
    )
    scene.stop("pais-sismico")


def _quake_shake(scene: Scene, mw: float, duration: float, *, seed: int):
    """Sacudida por trauma: el desplazamiento crece con el cuadrado del trauma."""
    trauma = 0.5 + 0.45 * _intensity(mw)
    return scene.camera.animate.shake(
        amplitude=0.14,
        trauma=trauma,
        decay=trauma / duration,
        frequency=12.0,
        rotation=0.006,
        seed=seed,
    )


# Proceso constructivo en el orden de obra, y lo que hace el conjunto en un sismo.
STEPS = (
    ("Cimiento y sobrecimiento", "Concreto ciclópeo bajo todos los muros"),
    ("Acero de columnas", "Se ancla al cimiento antes de asentar el muro"),
    ("Muro de ladrillo", "Extremos dentados y dinteles sobre los vanos"),
    ("Vaciado de columnas", "El concreto llena el dentado y amarra el muro"),
    ("Viga solera y losa", "Cierran el confinamiento y unen todos los muros"),
)
IN_QUAKE = (
    ("El sismo no tiene una dirección fija", "se idealiza con sus componentes en X y en Y"),
    ("La losa reparte la fuerza", "entre todos los muros, como un diafragma rígido"),
    ("La vivienda se deforma como unidad", "columnas y vigas soleras amarran cada paño"),
    ("Cada muro resiste en su plano", "por eso hacen falta muros en X y en Y"),
)
LIST_X, LIST_TOP, LIST_GAP = 0.9, 2.1, 0.92
DRIFT = 0.3  # m en la losa; exagerado para que se vea
# Diagrama del sismo sobre el terreno, frente a la fachada (m, en planta).
QUAKE_TAIL, QUAKE_REACH, QUAKE_ANGLE = (1.6, -2.27), 3.0, math.radians(35)


def _entry(
    scene: Scene, title: str, body: str, y: float, number: str | None = None
) -> Drawable:
    x = LIST_X + (0.55 if number else 0)
    parts: list[Drawable] = []
    if number:
        parts.append(numeral(scene, number, LIST_X, y + 0.04, size=0.36))
    parts.append(t(scene, title, x, y, size=0.24, weight=700, color=INK))
    parts.append(t(scene, body, x, y - 0.34, size=0.19, color=INK_SOFT))
    return scene.geometry.group(parts)


def _ground_vector(
    scene: Scene,
    iso: Iso,
    start: tuple[float, float],
    end: tuple[float, float],
    color: Color,
) -> Drawable:
    """Vector dibujado sobre el terreno, en coordenadas de planta."""
    (x0, y0), (x1, y1) = iso(*start, 0), iso(*end, 0)
    return (
        scene.geometry.arrow(
            x0, y0, x1, y1, head_length=0.2, head_width=0.2, body_width=0.05
        )
        .fill(color)
        .no_stroke()
    )


def _nudge(point: tuple[float, float], dx: float, dy: float) -> tuple[float, float]:
    return point[0] + dx, point[1] + dy


def _sway(house: House, dx: float, dy: float):
    """Vaivén amortiguado: cada hilada se desplaza en proporción a su altura."""
    swings = []
    previous = 0.0
    for amplitude in (1.0, -0.75, 0.5, -0.3, 0.12, 0.0):
        step = amplitude - previous
        swings.append(
            parallel(
                *[
                    layer.animate.shift_by(step * dx * share, step * dy * share)
                    .duration(0.36)
                    .easing(Easing.ease_in_out(EasingCurve.SINE))
                    for layer, share in house.layers
                ]
            )
        )
        previous = amplitude
    return sequence(*swings)


def seismic(scene: Scene) -> None:
    header(scene, KICKER, "Frente al sismo, la vivienda confinada trabaja como unidad")

    iso = Iso((-6.6, -0.33), 0.63)
    house = draw_house(scene, iso)
    heading = label(scene, "Proceso constructivo", LIST_X, 2.62, color=MUTED, size=0.14)
    steps = [
        _entry(scene, title, body, LIST_TOP - i * LIST_GAP, str(i + 1))
        for i, (title, body) in enumerate(STEPS)
    ]

    def enter(i: int):
        """Aparece el paso i y el anterior pasa a segundo plano."""
        anims = [steps[i].animate.fade_in_from(Direction.LEFT, 0.06).duration(0.35)]
        if i:
            anims.append(steps[i - 1].animate.opacity(0.35).duration(0.35))
        return anims

    # 1 · Cimiento corrido y sobrecimiento.
    scene.play(
        [
            heading.animate.fade_in().duration(0.3),
            *enter(0),
            house.ground.animate.fade_in().duration(0.4),
            stagger(
                *[
                    p.animate.fade_in_from(Direction.DOWN, 0.04).duration(0.3)
                    for p in house.footing + house.plinth
                ],
                each=0.04,
            ),
        ]
    )
    scene.wait(0.3)

    # 2 · El acero de las columnas sube desde el cimiento.
    scene.play(
        [
            *enter(1),
            stagger(
                *[g.animate.fade_in().duration(0.12) for g in house.steel], each=0.035
            ),
        ]
    )
    scene.wait(0.3)

    # 3 · Hilada por hilada; la cara superior acompaña a la última asentada.
    courses = []
    for k, bricks in enumerate(house.masonry):
        parts = [
            bricks.animate.fade_in_from(Direction.DOWN, 0.03).duration(0.14),
            house.tops[k].animate.fade_in().duration(0.08),
        ]
        if k:
            parts.append(house.tops[k - 1].animate.fade_out().duration(0.08))
        courses.append(parallel(*parts))
    scene.play([*enter(2), stagger(*courses, each=0.09)])
    scene.wait(0.3)

    # 4 · El concreto de las columnas sube y cubre el acero.
    scene.play(
        [
            *enter(3),
            stagger(
                *[
                    parallel(
                        pour.animate.fade_in().duration(0.12),
                        bars.animate.fade_out().duration(0.12),
                    )
                    for pour, bars in zip(house.concrete, house.steel)
                ],
                each=0.05,
            ),
        ]
    )
    scene.wait(0.3)

    # 5 · Viga solera y losa, vaciadas juntas.
    scene.play(
        [
            *enter(4),
            stagger(*[b.animate.fade_in().duration(0.3) for b in house.beams], each=0.05),
            house.steel[-1].animate.fade_out().duration(0.3),
        ]
    )
    scene.play(house.slab.animate.fill_level(1).duration(0.9))
    scene.play([s.animate.opacity(1).duration(0.4) for s in steps[:-1]])
    scene.stop("proceso-constructivo")

    # En el sismo: la dirección real es cualquiera; se idealiza con sus componentes
    # en X y en Y, y la vivienda completa se deforma junta en cada una.
    quake_heading = label(scene, "En un sismo", LIST_X, 2.62, color=MUTED, size=0.14)
    notes = [
        _entry(scene, title, body, LIST_TOP - i * LIST_GAP)
        for i, (title, body) in enumerate(IN_QUAKE)
    ]
    # Triángulo de vectores: el sismo es la hipotenusa; X e Y, los catetos.
    x0, y0 = QUAKE_TAIL
    corner = (x0 + QUAKE_REACH * math.cos(QUAKE_ANGLE), y0)
    tip = (corner[0], y0 + QUAKE_REACH * math.sin(QUAKE_ANGLE))
    quake = _ground_vector(scene, iso, QUAKE_TAIL, tip, INK_SOFT)
    x_comp = _ground_vector(scene, iso, QUAKE_TAIL, corner, BRICK)
    y_comp = _ground_vector(scene, iso, corner, tip, STEEL)

    def middle(p: tuple[float, float], q: tuple[float, float]) -> tuple[float, float]:
        return iso((p[0] + q[0]) / 2, (p[1] + q[1]) / 2, 0)

    quake_label = t(
        scene,
        "Sismo",
        *_nudge(middle(QUAKE_TAIL, tip), 0, 0.14),
        size=0.2,
        weight=700,
        color=INK_SOFT,
        anchor=Anchor.BOTTOM,
    )
    x_label = t(
        scene,
        "X",
        *_nudge(middle(QUAKE_TAIL, corner), -0.1, -0.1),
        size=0.24,
        weight=700,
        color=BRICK,
        anchor=Anchor.TOP_RIGHT,
    )
    y_label = t(
        scene,
        "Y",
        *_nudge(middle(corner, tip), 0.12, -0.1),
        size=0.24,
        weight=700,
        color=STEEL,
        anchor=Anchor.TOP_LEFT,
    )
    exaggerated = t(
        scene,
        "Deformación exagerada",
        LIST_X,
        LIST_TOP - len(IN_QUAKE) * LIST_GAP + 0.2,
        font=MONO,
        size=0.13,
        color=MUTED,
    )
    scene.play(
        [
            heading.animate.fade_out().duration(0.3),
            *[s.animate.fade_out().duration(0.3) for s in steps],
        ]
    )
    scene.play(
        [
            quake_heading.animate.fade_in().duration(0.3),
            notes[0].animate.fade_in_from(Direction.LEFT, 0.06).duration(0.35),
            quake.animate.grow_arrow().duration(0.6),
            quake_label.animate.fade_in().duration(0.3).delay(0.2),
        ]
    )
    scene.play(
        [
            x_comp.animate.grow_arrow().duration(0.5),
            x_label.animate.fade_in().duration(0.3).delay(0.3),
            y_comp.animate.grow_arrow().duration(0.5).delay(0.5),
            y_label.animate.fade_in().duration(0.3).delay(0.8),
            quake.animate.opacity(0.5).duration(0.4).delay(1.0),
        ]
    )
    scene.stop("componentes-del-sismo")

    scene.play(
        [
            y_comp.animate.opacity(0.25).duration(0.3),
            y_label.animate.opacity(0.25).duration(0.3),
            notes[1].animate.fade_in_from(Direction.LEFT, 0.06).duration(0.35),
            exaggerated.animate.fade_in().duration(0.3),
        ]
    )
    scene.play(
        [
            _sway(house, *iso.along(DRIFT, 0)),
            notes[2].animate.fade_in_from(Direction.LEFT, 0.06).duration(0.35).delay(0.7),
        ]
    )
    scene.play(
        [
            x_comp.animate.opacity(0.25).duration(0.3),
            x_label.animate.opacity(0.25).duration(0.3),
            y_comp.animate.opacity(1).duration(0.3),
            y_label.animate.opacity(1).duration(0.3),
            notes[3].animate.fade_in_from(Direction.LEFT, 0.06).duration(0.35),
        ]
    )
    scene.play(_sway(house, *iso.along(0, DRIFT)))
    scene.play(
        [
            x_comp.animate.opacity(1).duration(0.3),
            x_label.animate.opacity(1).duration(0.3),
        ]
    )
    takeaway(
        scene,
        "La E.070 exige densidad mínima de muros en ambas direcciones y buena conexión",
    )
    source(
        scene,
        "Tesis · §1.1 Problemática, p. 1; §3.1 Albañilería confinada, p. 21 (Gonzales, 1992; "
        "Tavera, 2014; San Bartolomé, 2018). Vivienda esquemática.",
    )
    scene.stop("vivienda-en-conjunto")


def manual_transfer(scene: Scene) -> None:
    header(scene, KICKER, "ETABS no verifica la E.070: se hace un proceso manual")

    # Ventana de resultados del modelo: valores reales de V_e, piso 1, MCT (tb:agriet_xy).
    piers = ["X1", "X3", "X4", "X5", "X6"]
    etabs = _window(
        scene, -5.15, 0.85, 3.9, 2.75, "ETABS · Pier Forces", icon=ETABS_ICON
    )
    head = ["Story", "Pier", "Ve (tonf)"]
    xs = [-6.8, -5.6, -4.3]
    table: list[Drawable] = [
        t(
            scene,
            h_,
            x,
            1.55,
            font=MONO,
            size=0.15,
            weight=700,
            color=INK_SOFT,
            anchor=Anchor.LEFT,
        )
        for h_, x in zip(head, xs, strict=True)
    ]
    records: list[list[Drawable]] = []
    for i, pier in enumerate(piers):
        y = 1.15 - i * 0.36
        cells: list[Drawable] = [
            t(
                scene,
                "Story1",
                xs[0],
                y,
                font=MONO,
                size=0.16,
                color=INK,
                anchor=Anchor.LEFT,
            ),
            t(
                scene,
                pier,
                xs[1],
                y,
                font=MONO,
                size=0.16,
                color=INK,
                anchor=Anchor.LEFT,
            ),
            t(
                scene,
                f"{CRACKING_FLOOR1['MCT'][pier][0]:.3f}",
                xs[2],
                y,
                font=MONO,
                size=0.16,
                color=INK,
                anchor=Anchor.LEFT,
            ),
        ]
        records.append(cells)
    sheet = _window(
        scene,
        4.4,
        0.85,
        4.6,
        2.75,
        "Excel · Verificación E.070",
        icon=EXCEL_ICON,
        tint=PASS_TINT,
    )
    letters = [
        t(
            scene,
            c,
            2.55 + i * 1.2,
            1.55,
            font=MONO,
            size=0.14,
            color=MUTED,
            anchor=Anchor.CENTER,
        )
        for i, c in enumerate("ABCD")
    ]
    grid = [
        scene.geometry.line(2.2, 1.35 - j * 0.36, 6.6, 1.35 - j * 0.36).stroke(
            FAINT, 0.01
        )
        for j in range(6)
    ] + [
        scene.geometry.line(
            2.2 + i * 1.2 - 0.05, 1.4, 2.2 + i * 1.2 - 0.05, -0.45
        ).stroke(FAINT, 0.01)
        for i in range(1, 4)
    ]
    scene.play(
        [
            etabs.animate.fade_in().duration(0.4),
            *[x.animate.fade_in().duration(0.4) for x in table],
        ]
    )
    scene.play(
        stagger(
            *[c.animate.fade_in().duration(0.2) for row in records for c in row],
            each=0.02,
        )
    )
    scene.play(
        [
            sheet.animate.fade_in().duration(0.4),
            *[x.animate.fade_in().duration(0.4) for x in letters + grid],
        ]
    )

    steps = [("exportar", -2.25), ("filtrar", -0.6), ("copiar", 1.05)]
    step_labels = [
        pill(
            scene,
            name,
            x,
            1.72,
            color=BRICK_DEEP,
            background=BRICK_SOFT,
            size=0.19,
            font=MONO,
        )
        for name, x in steps
    ]
    arrow = (
        scene.geometry.arrow(
            -3.0, 1.3, 1.9, 1.3, head_length=0.18, head_width=0.16, body_width=0.03
        )
        .fill(BRICK)
        .no_stroke()
    )
    scene.play(
        stagger(
            arrow.animate.grow_arrow().duration(0.4),
            *[p.animate.fade_in().duration(0.25) for p in step_labels],
            each=0.12,
        )
    )
    # Cada fila viaja de la tabla del modelo a la hoja; es la misma cifra, trasladada.
    moves = []
    for i, row in enumerate(records):
        y = 1.15 - i * 0.36
        copies = [
            t(
                scene,
                "1",
                2.55,
                y,
                font=MONO,
                size=0.16,
                color=INK,
                anchor=Anchor.CENTER,
            ),
            t(
                scene,
                piers[i],
                3.75,
                y,
                font=MONO,
                size=0.16,
                color=INK,
                anchor=Anchor.CENTER,
            ),
            t(
                scene,
                f"{CRACKING_FLOOR1['MCT'][piers[i]][0]:.3f}",
                4.95,
                y,
                font=MONO,
                size=0.16,
                color=INK,
                anchor=Anchor.CENTER,
            ),
        ]
        moves.append(
            sequence(
                *[r.animate.indicate().duration(0.3) for r in row[1:2]],
                *[
                    c.animate.fade_in_from(Direction.LEFT, 0.5).duration(0.35)
                    for c in copies
                ],
            )
        )
    scene.play(stagger(*moves, each=0.35))
    risks = [
        ("¿fila y Pier correctos?", -0.55, 0.65),
        ("¿combinación de carga?", -0.55, 0.15),
        ("¿unidades y signos?", -0.55, -0.35),
    ]
    risk_pills = [
        pill(
            scene,
            r,
            x,
            y,
            color=INK_SOFT,
            background=CARD,
            border=RULE,
            size=0.17,
            font="Lato",
        )
        for r, x, y in risks
    ]
    scene.play(
        stagger(
            *[
                p.animate.fade_in_from(Direction.UP, 0.08).duration(0.35)
                for p in risk_pills
            ],
            each=0.12,
        )
    )
    scene.stop("traslado-manual")

    loop = (
        scene.geometry.curved_arrow(
            4.4,
            -0.6,
            -5.15,
            -0.6,
            -0.3,
            head_length=0.16,
            head_width=0.16,
            body_width=0.028,
        )
        .fill(BRICK)
        .no_stroke()
    )
    loop_label = t(
        scene,
        "Si un muro no cumple: modificar el modelo, reanalizar y repetir el traslado",
        -0.4,
        -1.35,
        size=0.21,
        color=BRICK_DEEP,
        anchor=Anchor.TOP,
    )
    scene.play(
        [
            loop.animate.grow_arrow().duration(0.9),
            loop_label.animate.fade_in().duration(0.5),
        ]
    )
    question = panel(
        scene, 0, -2.55, 14.6, 0.8, fill=PAPER_DEEP, border=None
    )
    q_text = t(
        scene,
        "¿Cómo sistematizar la verificación de la norma E.070 a partir de un modelo de ETABS?",
        0,
        -2.55,
        font=DISPLAY,
        size=0.3,
        weight=700,
        color=INK,
        anchor=Anchor.CENTER,
    )
    scene.play(
        [
            question.animate.fade_in().duration(0.4),
            q_text.animate.fade_in_from(Direction.UP, 0.08).duration(0.6),
        ]
    )
    source(
        scene,
        "Tesis · §1.1 Problemática y §1.2 Justificación, pp. 1–2. Valores: $V_e$ del piso 1, MCT (Tabla 35, p. 86).",
    )
    scene.stop("pregunta-de-investigacion")


PASS_TINT = STEEL_SOFT
ETABS_ICON = ("E", "#2B6CB0")
EXCEL_ICON = ("X", "#107C41")


def _window(
    scene: Scene,
    cx: float,
    cy: float,
    w: float,
    h: float,
    title: str,
    *,
    icon: tuple[str, str],
    tint=CARD,
) -> Drawable:
    # Decoración de Windows (ETABS solo corre en Windows): esquinas casi rectas,
    # título a la izquierda y botones minimizar/maximizar/cerrar a la derecha.
    frame = (
        scene.geometry.rounded_rect(w, h, 0.04)
        .fill(CARD)
        .stroke(RULE, 0.014)
        .move_to(cx, cy)
    )
    bar_y = cy + h / 2 - 0.17
    bar = (
        scene.geometry.rounded_rect(w, 0.34, 0.04)
        .fill(tint)
        .no_stroke()
        .move_to(cx, bar_y)
    )
    g = 0.055  # semilado del glifo
    close_x = cx + w / 2 - 0.22
    max_x = close_x - 0.42
    min_x = max_x - 0.42
    controls = [
        scene.geometry.line(min_x - g, bar_y, min_x + g, bar_y).stroke(INK_SOFT, 0.012),
        scene.geometry.rect(2 * g, 2 * g)
        .no_fill()
        .stroke(INK_SOFT, 0.012)
        .move_to(max_x, bar_y),
        scene.geometry.line(
            close_x - g, bar_y - g, close_x + g, bar_y + g
        ).stroke(INK_SOFT, 0.012),
        scene.geometry.line(
            close_x - g, bar_y + g, close_x + g, bar_y - g
        ).stroke(INK_SOFT, 0.012),
    ]
    # Ícono de la aplicación, representativo (no el logotipo oficial).
    letter, color = icon
    icon_x = cx - w / 2 + 0.22
    badge = [
        scene.geometry.rounded_rect(0.22, 0.22, 0.04)
        .fill(color)
        .no_stroke()
        .move_to(icon_x, bar_y),
        t(
            scene,
            letter,
            icon_x,
            bar_y,
            font="Lato",
            size=0.15,
            weight=900,
            color="#FFFFFF",
            anchor=Anchor.CENTER,
        ),
    ]
    name = t(
        scene,
        title,
        icon_x + 0.22,
        bar_y,
        font=MONO,
        size=0.14,
        color=INK_SOFT,
        anchor=Anchor.LEFT,
    )
    return scene.geometry.group([frame, bar, *controls, *badge, name])


SECTION = Section(
    "problematica",
    [
        SectionStep(
            name="Problemática · material",
            build=materials,
            transition=Transition.cross_fade(0.45),
            notes=(
                "45 s. INEI, Censos Nacionales 2025, viviendas particulares con ocupantes: "
                "61.8 % declara paredes de ladrillo o bloque de concreto (la tesis citaba INEI "
                "2017; se actualizó el dato). Aclarar que el material no acredita confinamiento "
                "ni desempeño: solo muestra la relevancia del sistema. El relleno del mapa es "
                "ilustrativo, no una distribución geográfica."
            ),
        ),
        SectionStep(
            name="Problemática · país sísmico",
            build=plates,
            transition=Transition.cross_fade(0.45),
            notes=(
                "50 s. (1) Ubicar el Perú. (2) Frente a la costa corre la fosa Perú-Chile: al "
                "oeste la placa de Nazca, al este la Sudamericana, sobre la que está todo el país. "
                "Nazca avanza hacia el continente unos 7–8 cm/año (verificar la cifra con Tavera, "
                "2014). (3) Acercamiento a la fosa frente a Lima: el bloque muestra que Nazca se "
                "hunde bajo la Sudamericana; el contacto se traba, acumula energía y la libera en "
                "sismos. (4) De vuelta al mapa: por eso los grandes sismos están frente a la costa: "
                "Lima 1940 (tras él llegó la albañilería confinada), Áncash 1970, Arequipa 2001, "
                "Pisco 2007. Fosa y epicentros son aproximados."
            ),
        ),
        SectionStep(
            name="Problemática · sistema sísmico",
            build=seismic,
            transition=Transition.cross_fade(0.45),
            notes=(
                "60 s. La albañilería confinada llegó tras el terremoto de Lima de 1940. (1) Seguir "
                "la obra en orden: cimiento y sobrecimiento; el acero de las columnas se ancla "
                "antes del muro; el muro se asienta con los extremos dentados; luego se vacían las "
                "columnas contra el dentado y, al final, la viga solera junto con la losa "
                "(Gonzales, 1992; San Bartolomé, 2018). Puerta y ventana llevan columnas a los "
                "lados y dintel. (2) El sismo llega en cualquier dirección; para el análisis se "
                "descompone en sus componentes X e Y (triángulo sobre el terreno). (3) En cada "
                "componente la losa reparte la fuerza y columnas y soleras amarran cada paño: la "
                "vivienda se deforma como unidad y gana "
                "ductilidad. Cada muro resiste en su plano: en X trabaja la fachada; en Y, los "
                "muros laterales. Por eso la E.070 pide densidad mínima de muros en ambas "
                "direcciones y conexión con los confinamientos. La deformación está exagerada."
            ),
        ),
        SectionStep(
            name="Problemática · traslado manual",
            build=manual_transfer,
            transition=Transition.cross_fade(0.45),
            notes=(
                "1.25 min. Los programas comerciales (ETABS, SAP2000) no implementan la E.070; el "
                "ingeniero exporta tablas, filtra, copia a hojas de cálculo y verifica. Las cifras "
                "son V_e reales del piso 1 del modelo MCT (Tabla 35 (p. 86)), usadas solo para ilustrar "
                "el traslado. Riesgos citados en la tesis: errores de selección, transcripción, "
                "ordenamiento y verificaciones omitidas; no se midió su frecuencia. Cerrar con la "
                "pregunta de investigación."
            ),
        ),
    ],
)
