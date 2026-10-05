"""Bloque 1 · Problemática: material, sistema sísmico y traslado manual de datos."""

import math
from dataclasses import dataclass

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

from tesis.components import header, source, takeaway_at
from tesis.data.materiales_inei import (
    MATERIALES_ORDENADOS,
    SOURCE_LABEL,
    TOTAL_VIVIENDAS,
)
from tesis.data.sudamerica import COUNTRIES, Ring
from tesis.data.sudamerica import SOURCE_LABEL as OUTLINES_SOURCE
from tesis.data.thesis import CRACKING_FLOOR1
from tesis.kit import (
    dash,
    label,
    numeral,
    t,
)
from tesis.theme import (
    BRICK,
    BRICK_DEEP,
    BRICK_SOFT,
    CARD,
    DISPLAY,
    FAIL,
    FAIL_SOFT,
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
    header(
        scene, KICKER, "El ladrillo es el material usado en seis de cada diez viviendas"
    )

    outline = (
        scene.media.svg("peru.svg")
        .no_fill()
        .stroke(INK_SOFT, 0.0093)
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
        f"{SOURCE_LABEL} · Características de la vivienda."
    )
    scene.stop("materiales-listo")


# Mapa de placas en Mercator, a todo el ancho útil y del título a la fuente. El alto
# del marco va de 1° N a 19° S y fija la escala; MAP_LON es la longitud que cae en x = 0, de modo que la
# fosa quede cerca del centro: Nazca a la izquierda, la Sudamericana a la derecha.
MAP_LEFT, MAP_RIGHT, MAP_TOP, MAP_BOTTOM = -7.3, 7.3, 2.73, -3.5
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
    peru = scene.geometry.group(
        _outline(scene, COUNTRIES["PER"], CARD, INK_SOFT, 0.014)
    )
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
        scene,
        "Perú",
        *_geo(-74.4, -4.9),
        size=0.2,
        color=INK_SOFT,
        anchor=Anchor.CENTER,
    )
    places = [
        label(
            scene, name, *_geo(lon, lat), size=0.12, color=MUTED, anchor=Anchor.CENTER
        )
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

    # La placa de Nazca converge hacia el este-noreste, contra el continente. En cada
    # carril una flecha avanza a velocidad constante y se desvanece mientras sale la
    # siguiente, como la placa que se mueve; la última se queda para la pausa.
    body_dx, body_dy = 1.2, 0.24  # de la cola a la punta
    # Cada flecha recorre algo más que su largo: la siguiente no la alcanza.
    travel = 1.3 / math.hypot(body_dx, body_dy)
    step_x, step_y = body_dx * travel, body_dy * travel
    cycle, departures = 1.0, (0.0, 0.9, 1.8)
    flow = []
    for lane, lat in enumerate((-9.5, -15.0)):
        x1, y1 = _geo(-83.2, lat)
        for k, departure in enumerate(departures):
            arrow = (
                scene.geometry.arrow(
                    x1 - body_dx,
                    y1 - body_dy,
                    x1,
                    y1,
                    head_length=0.2,
                    head_width=0.22,
                    body_width=0.07,
                )
                .fill(STEEL)
                .no_stroke()
                .shift_by(-step_x, -step_y)
            )
            stays = k == len(departures) - 1
            motion = [
                arrow.animate.shift_by(step_x, step_y)
                .duration(cycle)
                .easing(Easing.ease_out(EasingCurve.SINE) if stays else Easing.LINEAR),
                arrow.animate.fade_in().duration(0.3 * cycle),
            ]
            if not stays:
                motion.append(
                    arrow.animate.fade_out().duration(0.35 * cycle).delay(0.65 * cycle)
                )
            flow.append(parallel(*motion).delay(departure + 0.2 * lane))
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
            *flow,
            rate.animate.fade_in().duration(0.5).delay(1.6),
        ]
    )
    scene.stop("dos-placas")

    # Mecanismo: una segunda cámara mira la fosa frente a Lima y su pantalla brota de
    # ahí sobre el océano; dentro, un corte en 3D sustituye al mapa. El corte vive en
    # una capa que solo ve esa pantalla, así que el mapa sigue a la vista alrededor.
    # Lo de adentro se diseña en unidades de la pantalla (origen en su centro) y se
    # lleva a la escena dividiendo por el aumento.
    lens = 3.5  # aumento de la pantalla del corte
    cx, cy = _geo(-78.4, -12.0)
    screen_w, screen_h = 6.4, 3.6

    def inside(sx: float, sy: float) -> tuple[float, float]:
        return cx + sx / lens, cy + sy / lens

    veil = (
        scene.geometry.rect(screen_w / lens + 0.1, screen_h / lens + 0.1)
        .fill(PAPER)
        .no_stroke()
        .move_to(cx, cy)
        .z_index(30)
    )
    block_scale, block_y = 0.40, 0.25
    block = scene.media.lottie("placas_subduccion_paleta.lottie")
    block.scale_by(block_scale / lens).move_to(*inside(0, block_y)).z_index(31)
    block_labels = [
        t(
            scene,
            name,
            *inside(dx * block_scale, block_y + dy * block_scale),
            font=MONO,
            size=0.15 / lens,
            weight=700,
            color=color,
            anchor=Anchor.CENTER,
        ).z_index(31)
        for name, dx, dy, color in (
            ("NAZCA", -4.33, 2.25, STEEL),
            ("SUDAMERICANA", 4.8, 2.98, INK_SOFT),
        )
    ]
    explain = t(
        scene,
        "La placa de Nazca subduce bajo la Sudamericana.\n"
        "Acumula energía y la libera en sismos.",
        *inside(0, -1.3),
        size=0.165 / lens,
        color=INK_SOFT,
        anchor=Anchor.TOP,
    ).z_index(31)
    section_view = [veil, block, *block_labels, explain]
    for part in section_view:
        part.view_layer("corte")
    cut = scene.camera.inset(
        (cx, cy),
        zoom=lens,
        at=(-3.7, 0.2),  # cubre las puntas de las flechas y el rótulo de la fosa
        size=screen_w,
        shape="rect",
        color=INK_SOFT,
        layers=["corte"],
    )
    scene.play(
        cut.animate.pop_out()
        .duration(1.0)
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
    # El corte se apaga y la pantalla vuelve a la fosa.
    scene.play(
        sequence(
            parallel(*[p.animate.fade_out().duration(0.4) for p in section_view]),
            cut.animate.pop_in().duration(0.6),
        )
    )

    # Grandes sismos del último siglo: todos frente a la costa, sobre el contacto.
    marks = []
    for name, year, mw, lon, lat in QUAKES:
        x, y = _geo(lon, lat)
        dot = (
            scene.geometry.circle(0.07).fill(FAIL).no_stroke().move_to(x, y).z_index(5)
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
            scene,
            name,
            x + 0.19,
            y + 0.2,
            size=0.17,
            weight=700,
            color=INK,
            anchor=Anchor.LEFT,
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
    # La cámara entra en la costa y la recorre de norte a sur, sacudiendo la escena en
    # cada evento con un trauma proporcional a la magnitud: Arequipa (8.4) sacude
    # visiblemente más que Áncash (7.9). El encuadre no sale del mapa y al final
    # vuelve a la vista completa.
    zoom = 3.0
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
                .duration(
                    1.2 if i == 0 else 0.8
                )  # el primero parte de la vista completa
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
    (
        "El sismo no tiene una dirección fija",
        "se idealiza con sus componentes en X y en Y",
    ),
    ("La losa reparte la fuerza", "entre todos los muros, como un diafragma rígido"),
    (
        "La vivienda se deforma como unidad",
        "columnas y vigas soleras amarran cada paño",
    ),
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
            stagger(
                *[b.animate.fade_in().duration(0.3) for b in house.beams], each=0.05
            ),
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
            notes[2]
            .animate.fade_in_from(Direction.LEFT, 0.06)
            .duration(0.35)
            .delay(0.7),
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
    takeaway_at(
        scene,
        "La E.070 exige densidad mínima de muros en ambas direcciones y buena conexión",
    )
    source(
        scene,
        "Tesis · §1.1 Problemática, p. 1; §3.1 Albañilería confinada, p. 21 (Gonzales, 1992; "
        "Tavera, 2014; San Bartolomé, 2018). Vivienda esquemática.",
    )
    scene.stop("vivienda-en-conjunto")


# Normas de diseño de muros que ofrece ETABS (extracto, con sus nombres en el
# programa): todas de concreto armado y extranjeras; la E.070 no figura.
ETABS_WALL_CODES = (
    "ACI 318-19",
    "AS 3600-2018",
    "BS 8110-97",
    "CSA A23.3-19",
    "Eurocode 2-2004",
    "Indian IS 456:2000",
    "Mexican RCDF 2017",
    "NZS 3101:2006",
)
ETABS_OFFER = (
    ("Normas de concreto armado", "ACI, Eurocódigo, CSA, NZS: todas extranjeras"),
    ("Ninguna de albañilería", "la E.070 no está implementada en el programa"),
    ("La verificación queda fuera", "se resuelve a mano en hojas de cálculo"),
)
# Riesgos del traslado manual con los términos de la tesis (§1.1 y cap. 6).
TRANSFER_RISKS = (
    "Errores de selección",
    "Errores de transcripción",
    "Errores de ordenamiento",
    "Verificaciones omitidas",
)
TRANSFER_PIERS = ("X1", "X3", "X4", "X5", "X6", "X7")
# Vueltas del traslado. La última copia los valores reales (MCT, piso 1, Tabla 35);
# las previas son ilustrativas: X1 no cumple, se agranda en el modelo y, más rígido,
# atrae más cortante y deja algo menos a los demás muros.
X1_EARLIER = (
    (6.214, 5.873),
    (6.688, 6.502),
)  # (Ve, 0.55 Vm) de X1 en las vueltas 1 y 2
OTHERS_EARLIER = (1.046, 1.022)  # Ve de los demás muros respecto del valor final

type Span = tuple[float, float, float]


def _transfer_round(r: int) -> dict[str, tuple[float, float]]:
    """(Ve, 0.55 Vm) de cada muro del traslado en la vuelta ``r``, desde 0."""
    final = CRACKING_FLOOR1["MCT"]
    if r == len(X1_EARLIER):
        return {pier: final[pier] for pier in TRANSFER_PIERS}
    values = {
        pier: (final[pier][0] * OTHERS_EARLIER[r], final[pier][1])
        for pier in TRANSFER_PIERS
    }
    values["X1"] = X1_EARLIER[r]
    return values


@dataclass(frozen=True)
class Transcript:
    """Una vuelta del traslado: lo copiado a mano en Excel y Mathcad."""

    rows: list[list[Drawable]]  # por fila de Excel: Ve, 0.55 Vm y Cumple
    sheet: list[Drawable]  # V_e y la comprobación en Mathcad
    spans: list[Span]  # tramos (x0, x1, y) de lo copiado, en el orden de ``pasted``

    @property
    def pasted(self) -> list[Drawable]:
        return [cell for row in self.rows for cell in row[:2]] + self.sheet


def _copied(
    scene: Scene,
    content: str,
    x: float,
    y: float,
    *,
    size: float,
    font: str | None = None,
    color: Color = INK,
) -> tuple[Drawable, Span]:
    """Valor copiado a mano y su tramo, que se tacha cuando queda desactualizado."""
    text = t(
        scene, content, x, y, font=font, size=size, color=color, anchor=Anchor.LEFT
    )
    box = text.bounds()
    return text, (box.left, box.right, y)


def _cells(
    scene: Scene,
    values: tuple[str, ...],
    xs: tuple[float, ...],
    y: float,
    *,
    weight: int = 400,
    color: Color = INK,
    size: float = 0.15,
) -> list[Drawable]:
    return [
        t(
            scene,
            v,
            x,
            y,
            font=MONO,
            size=size,
            weight=weight,
            color=color,
            anchor=Anchor.LEFT,
        )
        for v, x in zip(values, xs, strict=True)
    ]


def _arc(
    p: tuple[float, float], q: tuple[float, float], *, sag: float, samples: int = 48
) -> list[tuple[float, float]]:
    """Arco circular de ``p`` a ``q`` que se comba ``sag`` por debajo de la cuerda."""
    (x0, y0), (x1, y1) = p, q
    chord = math.hypot(x1 - x0, y1 - y0)
    nx, ny = -(y1 - y0) / chord, (x1 - x0) / chord
    if ny > 0:
        nx, ny = -nx, -ny  # normal hacia abajo
    radius = (chord**2 / 4 + sag**2) / (2 * sag)
    cx = (x0 + x1) / 2 - nx * (radius - sag)
    cy = (y0 + y1) / 2 - ny * (radius - sag)
    a0 = math.atan2(y0 - cy, x0 - cx)
    sweep = (math.atan2(y1 - cy, x1 - cx) - a0 + math.pi) % (2 * math.pi) - math.pi
    return [
        (
            cx + radius * math.cos(a0 + sweep * i / samples),
            cy + radius * math.sin(a0 + sweep * i / samples),
        )
        for i in range(samples + 1)
    ]


def _arrow_head(
    scene: Scene,
    tail: tuple[float, float],
    tip: tuple[float, float],
    color: Color,
    *,
    length: float = 0.18,
    width: float = 0.18,
) -> Drawable:
    """Punta de flecha en ``tip`` orientada según el último tramo del trazo."""
    ux, uy = tip[0] - tail[0], tip[1] - tail[1]
    norm = math.hypot(ux, uy)
    ux, uy = ux / norm, uy / norm
    bx, by = tip[0] - ux * length, tip[1] - uy * length
    return (
        scene.geometry.polygon(
            [
                tip,
                (bx - uy * width / 2, by + ux * width / 2),
                (bx + uy * width / 2, by - ux * width / 2),
            ]
        )
        .fill(color)
        .no_stroke()
    )


def _packets(
    scene: Scene,
    count: int,
    start: tuple[float, float],
    fork: tuple[float, float],
    targets: tuple[tuple[float, float], ...],
    *,
    each: float,
):
    """Filas que recorren el tronco y se reparten entre los destinos."""
    trips = []
    for i in range(count):
        packet = (
            scene.geometry.rect(0.32, 0.07)
            .fill(BRICK)
            .no_stroke()
            .move_to(*start)
            .z_index(5)
        )
        trips.append(
            sequence(
                packet.animate.fade_in().duration(0.08),
                packet.animate.move_to(*fork).duration(0.45),
                packet.animate.move_to(*targets[i % len(targets)]).duration(0.25),
                packet.animate.fade_out().duration(0.08),
                gap=0.01,
            )
        )
    return stagger(*trips, each=each)


def manual_transfer(scene: Scene) -> None:
    header(scene, KICKER, "ETABS no verifica la norma E.070: se hace un proceso manual")

    # 1 · La lista de normas de diseño de muros no incluye la E.070.
    dialog = _window(
        scene,
        -3.9,
        0.2,
        6.4,
        4.6,
        "ETABS · Shear Wall Design Preferences",
        icon=ETABS_ICON,
    )
    field_x0, field_x1, row_h = -4.6, -1.0, 0.34
    field_cx, field_w = (field_x0 + field_x1) / 2, field_x1 - field_x0
    code_label = t(
        scene,
        "Design Code",
        -6.8,
        1.75,
        font=MONO,
        size=0.15,
        color=INK_SOFT,
        anchor=Anchor.LEFT,
    )
    field = (
        scene.geometry.rect(field_w, row_h)
        .fill(CARD)
        .stroke(RULE, 0.014)
        .move_to(field_cx, 1.75)
    )
    chevron = (
        scene.geometry.polygon([(-1.3, 1.8), (-1.14, 1.8), (-1.22, 1.7)])
        .fill(INK_SOFT)
        .no_stroke()
    )
    current = t(
        scene,
        ETABS_WALL_CODES[0],
        field_x0 + 0.15,
        1.75,
        font=MONO,
        size=0.16,
        anchor=Anchor.LEFT,
    )
    list_top = 1.75 - row_h / 2 - 0.04
    list_box = (
        scene.geometry.rect(field_w, row_h * len(ETABS_WALL_CODES))
        .fill(CARD)
        .stroke(RULE, 0.014)
        .move_to(field_cx, list_top - row_h * len(ETABS_WALL_CODES) / 2)
    )
    row_y = [list_top - row_h * (i + 0.5) for i in range(len(ETABS_WALL_CODES) + 1)]
    scan = (
        scene.geometry.rect(field_w - 0.04, row_h - 0.04).fill(STEEL_SOFT).no_stroke()
    )
    scan.move_to(field_cx, row_y[0])
    codes = [
        t(
            scene,
            code,
            field_x0 + 0.15,
            y,
            font=MONO,
            size=0.15,
            color=INK,
            anchor=Anchor.LEFT,
        )
        for code, y in zip(ETABS_WALL_CODES, row_y, strict=False)
    ]
    # El hueco donde debería estar la norma peruana de albañilería.
    gap_y = row_y[-1] - 0.12
    corners = [
        (field_x0, gap_y + row_h / 2),
        (field_x1, gap_y + row_h / 2),
        (field_x1, gap_y - row_h / 2),
        (field_x0, gap_y - row_h / 2),
    ]
    missing_box = [
        scene.geometry.dashed_line(*p, *q, dash_length=0.07, gap_length=0.05).stroke(
            FAIL, 0.014
        )
        for p, q in zip(corners, corners[1:] + corners[:1], strict=True)
    ]
    missing = t(
        scene,
        "E.070 · Albañilería",
        field_x0 + 0.15,
        gap_y,
        font=MONO,
        size=0.15,
        color=FAIL,
        anchor=Anchor.LEFT,
    )
    missing_note = t(
        scene,
        "no disponible",
        field_x1 - 0.12,
        gap_y,
        size=0.15,
        weight=700,
        color=FAIL,
        anchor=Anchor.RIGHT,
    )
    offer_heading = label(
        scene, "Lo que ofrece ETABS", LIST_X, 2.62, color=MUTED, size=0.14
    )
    offer = [
        _entry(scene, title, body, LIST_TOP - i * LIST_GAP)
        for i, (title, body) in enumerate(ETABS_OFFER)
    ]
    scene.play(
        stagger(
            dialog.animate.fade_in().duration(0.4),
            parallel(
                code_label.animate.fade_in().duration(0.3),
                field.animate.fade_in().duration(0.3),
                chevron.animate.fade_in().duration(0.3),
                current.animate.fade_in().duration(0.3),
            ),
            parallel(
                list_box.animate.fade_in().duration(0.3),
                stagger(*[c.animate.fade_in().duration(0.2) for c in codes], each=0.05),
            ),
            each=0.25,
        )
    )
    # Un resaltado recorre la lista buscando la E.070 y termina en el hueco.
    scene.play(
        [
            offer_heading.animate.fade_in().duration(0.3),
            offer[0].animate.fade_in_from(Direction.LEFT, 0.06).duration(0.35),
            sequence(
                scan.animate.fade_in().duration(0.15),
                *[
                    scan.animate.move_to(field_cx, y).duration(0.16)
                    for y in row_y[1 : len(ETABS_WALL_CODES)]
                ],
                scan.animate.move_to(field_cx, gap_y).duration(0.2),
                parallel(
                    scan.animate.fill(FAIL_SOFT).duration(0.25),
                    *[d.animate.create().duration(0.3) for d in missing_box],
                    missing.animate.fade_in().duration(0.3),
                ),
                gap=0.01,
            ),
        ]
    )
    scene.play(
        [
            missing_note.animate.fade_in().duration(0.3),
            offer[1].animate.fade_in_from(Direction.LEFT, 0.06).duration(0.35),
            offer[2]
            .animate.fade_in_from(Direction.LEFT, 0.06)
            .duration(0.35)
            .delay(0.3),
        ]
    )
    scene.stop("sin-e070")

    # 2 · El ingeniero traslada las tablas del modelo a Excel o Mathcad.
    first: list[Drawable] = [
        dialog,
        code_label,
        field,
        chevron,
        current,
        list_box,
        scan,
        *codes,
        *missing_box,
        missing,
        missing_note,
        offer_heading,
        *offer,
    ]
    tables = [
        # Cada ventana asoma su barra de título completa detrás de la siguiente.
        _window(scene, -5.0 + d, 0.5 + 2.4 * d, 4.2, 2.9, name, icon=ETABS_ICON)
        for d, name in (
            (0.3, "ETABS · Story Drifts"),
            (0.15, "ETABS · Pier Section Properties"),
            (0.0, "ETABS · Pier Forces"),
        )
    ]
    etabs_xs = (-6.8, -5.55, -4.3)
    etabs_ys = [1.15 - i * 0.3 for i in range(len(TRANSFER_PIERS))]
    etabs_rows = [
        _cells(
            scene,
            ("Story", "Pier", "Ve (tonf)"),
            etabs_xs,
            1.5,
            weight=700,
            color=INK_SOFT,
        )
    ]
    etabs_rows += [
        _cells(scene, ("Story1", pier), etabs_xs[:2], y)
        for pier, y in zip(TRANSFER_PIERS, etabs_ys, strict=True)
    ]
    rounds = [_transfer_round(r) for r in range(len(X1_EARLIER) + 1)]
    # Ve de cada vuelta: cambian cada vez que se reanaliza el modelo modificado.
    etabs_ve = [
        [
            t(
                scene,
                f"{values[pier][0]:.3f}",
                etabs_xs[2],
                y,
                font=MONO,
                size=0.15,
                anchor=Anchor.LEFT,
            )
            for pier, y in zip(TRANSFER_PIERS, etabs_ys, strict=True)
        ]
        for values in rounds
    ]
    etabs_more = t(
        scene, "⋮", -5.55, -0.7, font=MONO, size=0.16, color=MUTED, anchor=Anchor.LEFT
    )
    # count = t(
    #     scene,
    #     "24 muros × 4 pisos = 96 filas por tabla y combinación",
    #     -7.1,
    #     -1.2,
    #     font=MONO,
    #     size=0.14,
    #     color=MUTED,
    # )

    trunk_y, fork_x = 0.5, 0.0
    trunk = scene.geometry.line(-2.45, trunk_y, fork_x, trunk_y).stroke(BRICK, 0.03)
    branches = [
        scene.geometry.arrow(
            fork_x, trunk_y, 1.2, y, head_length=0.16, head_width=0.16, body_width=0.03
        )
        .fill(BRICK)
        .no_stroke()
        for y in (1.3, -0.35)
    ]
    steps = t(
        scene,
        "exportar · filtrar · copiar",
        -1.22,
        trunk_y + 0.2,
        font=MONO,
        size=0.15,
        color=BRICK_DEEP,
        anchor=Anchor.BOTTOM,
    )
    excel = _window(
        scene,
        4.2,
        1.35,
        5.8,
        1.9,
        "Excel · Verificación E.070",
        icon=EXCEL_ICON,
        tint=PASS_TINT,
    )
    excel_xs = (1.55, 2.5, 3.5, 4.75, 6.1)
    excel_piers = TRANSFER_PIERS[:3]
    excel_ys = [1.5 - i * 0.28 for i in range(len(excel_piers))]
    excel_rows = [
        _cells(
            scene,
            ("Piso", "Muro", "Ve", "0.55 Vm", "Cumple"),
            excel_xs,
            1.8,
            weight=700,
            color=INK_SOFT,
        )
    ]
    excel_rows += [
        _cells(scene, ("1", pier), excel_xs[:2], y)
        for pier, y in zip(excel_piers, excel_ys, strict=True)
    ]
    excel_more = t(
        scene, "⋮", 2.5, 0.62, font=MONO, size=0.16, color=MUTED, anchor=Anchor.LEFT
    )
    mathcad = _window(
        scene, 4.2, -0.75, 5.8, 1.9, "Mathcad · Verificación E.070", icon=MATHCAD_ICON
    )
    vm_line = t(
        scene,
        "$V_m := 0.5 v'_m alpha t L + 0.23 P_g$",
        1.6,
        -0.82,
        size=0.19,
        color=INK,
        anchor=Anchor.LEFT,
    )

    def transcribe(values: dict[str, tuple[float, float]]) -> Transcript:
        """Lo que se copia en una vuelta; la hoja recalcula Cumple y Mathcad la comprobación."""
        rows: list[list[Drawable]] = []
        spans: list[Span] = []
        for pier, y in zip(excel_piers, excel_ys, strict=True):
            ve, cap = values[pier]
            ok = ve <= cap
            ve_text, ve_span = _copied(
                scene,
                f"{ve:.3f}",
                excel_xs[2],
                y,
                font=MONO,
                size=0.15,
                color=INK if ok else FAIL,
            )
            cap_text, cap_span = _copied(
                scene, f"{cap:.3f}", excel_xs[3], y, font=MONO, size=0.15
            )
            check = t(
                scene,
                "sí" if ok else "no",
                excel_xs[4],
                y,
                font=MONO,
                size=0.15,
                weight=400 if ok else 700,
                color=INK if ok else FAIL,
                anchor=Anchor.LEFT,
            )
            rows.append([ve_text, cap_text, check])
            spans += [ve_span, cap_span]
        ve, cap = values["X1"]
        ok = ve <= cap
        relation = "<=" if ok else ">"
        sheet: list[Drawable] = []
        for line, y, color in (
            (f'$V_e := {ve:.3f} "tonf"$', -0.42, INK),
            (
                f'$V_e {relation} 0.55 V_m = {cap:.3f} "tonf"$',
                -1.22,
                INK if ok else FAIL,
            ),
        ):
            text, span = _copied(scene, line, 1.6, y, size=0.19, color=color)
            sheet.append(text)
            spans.append(span)
        return Transcript(rows, sheet, spans)

    transcripts = [transcribe(values) for values in rounds]
    first_copy = transcripts[0]
    worksheet = [first_copy.sheet[0], vm_line, first_copy.sheet[1]]
    mathcad_more = t(
        scene, "⋮", 1.6, -1.52, font=MONO, size=0.16, color=MUTED, anchor=Anchor.LEFT
    )
    # risks = [
    #     label(scene, "Errores comunes", -2.38, 0.0, color=MUTED, size=0.14)
    # ] + [
    #     item
    #     for i, text in enumerate(TRANSFER_RISKS)
    #     for item in (
    #         dash(scene, -2.3, -0.42 - i * 0.34, color=INK_SOFT),
    #         t(
    #             scene,
    #             text,
    #             -2.12,
    #             -0.42 - i * 0.34,
    #             size=0.18,
    #             color=INK_SOFT,
    #             anchor=Anchor.LEFT,
    #         ),
    #     )
    # ]

    scene.play([d.animate.fade_out().duration(0.35) for d in first])
    scene.play(
        [
            stagger(
                *[
                    w.animate.fade_in_from(Direction.UP, 0.06).duration(0.35)
                    for w in tables
                ],
                each=0.15,
            ),
            stagger(
                *[
                    c.animate.fade_in().duration(0.15)
                    for c in etabs_rows[0]
                    + [
                        c
                        for row, ve in zip(etabs_rows[1:], etabs_ve[0], strict=True)
                        for c in (*row, ve)
                    ]
                ],
                each=0.02,
            ).delay(0.4),
            etabs_more.animate.fade_in().duration(0.2).delay(1.0),
            # count.animate.fade_in().duration(0.3).delay(1.1),
        ]
    )
    scene.play(
        [
            trunk.animate.create().duration(0.4),
            *[b.animate.grow_arrow().duration(0.4).delay(0.3) for b in branches],
            steps.animate.fade_in().duration(0.3).delay(0.2),
            excel.animate.fade_in().duration(0.4).delay(0.4),
            mathcad.animate.fade_in().duration(0.4).delay(0.5),
        ]
    )
    # Las filas viajan una a una por el mismo camino hacia la hoja o el documento.
    trip = ((-2.5, trunk_y), (fork_x, trunk_y), ((1.25, 1.3), (1.25, -0.35)))
    scene.play(
        [
            _packets(scene, 18, *trip, each=0.13),
            stagger(
                *[
                    c.animate.fade_in().duration(0.15)
                    for c in excel_rows[0]
                    + [
                        c
                        for row, copy in zip(
                            excel_rows[1:], first_copy.rows, strict=True
                        )
                        for c in (*row, *copy)
                    ]
                ],
                each=0.05,
            ).delay(0.6),
            excel_more.animate.fade_in().duration(0.2).delay(1.9),
            stagger(
                *[
                    w.animate.fade_in_from(Direction.LEFT, 0.06).duration(0.3)
                    for w in worksheet
                ],
                each=0.45,
            ).delay(0.8),
            mathcad_more.animate.fade_in().duration(0.2).delay(2.2),
        ]
    )
    # scene.play(stagger(*[r.animate.fade_in().duration(0.25) for r in risks], each=0.08))
    scene.stop("traslado-manual")

    # 3 · Si algo no cumple, se modifica el modelo y el traslado empieza de nuevo.
    # La flecha de regreso es un arco propio: un punto la recorre en cada vuelta.
    loop_path = _arc((4.2, -1.8), (-5.0, -1.5), sag=0.38)
    loop = scene.geometry.polyline(loop_path).no_fill().stroke(BRICK, 0.028)
    loop_head = _arrow_head(scene, loop_path[-2], loop_path[-1], BRICK)
    loop_label = t(
        scene,
        "Si un muro no cumple: modificar el modelo, reanalizar y repetir el traslado",
        -0.4,
        -2.14,
        size=0.2,
        color=BRICK_DEEP,
        anchor=Anchor.TOP,
    )
    change = (
        scene.geometry.circle(0.07)
        .fill(BRICK)
        .no_stroke()
        .move_to(*loop_path[0])
        .z_index(6)
    )
    # Contador de vueltas: anillo con flecha que gira una vez por iteración.
    badge = (-0.7, 1.75)  # arriba al centro, sobre el traslado que se repite
    # Sin pivote, el arco giraría alrededor del origen de la escena.
    ring = (
        scene.geometry.curved_arrow_arc(
            *badge,
            0.38,
            math.radians(110),
            math.radians(300),
            head_length=0.17,
            head_width=0.17,
            body_width=0.036,
        )
        .fill(BRICK)
        .no_stroke()
        .with_pivot(*badge)
    )
    turns = scene.viz.rolling_number(
        1, font_family=DISPLAY, weight=700, font_size=0.34, color=BRICK_DEEP
    )
    turns.move_to(*badge, Anchor.CENTER)
    scene.play(
        [
            # *[r.animate.opacity(0.35).duration(0.3) for r in risks],
            loop.animate.create().duration(0.8),
            loop_head.animate.fade_in().duration(0.2).delay(0.7),
            loop_label.animate.fade_in().duration(0.5).delay(0.4),
            ring.animate.fade_in().duration(0.3).delay(0.6),
            turns.visual.animate.fade_in().duration(0.3).delay(0.6),
        ]
    )
    # Cada vuelta: el cambio viaja al modelo, lo copiado queda tachado, ETABS
    # reanaliza (barra de progreso) con nuevos Ve y se vuelve a copiar todo.
    for n in range(1, len(rounds)):
        before, after = transcripts[n - 1], transcripts[n]
        strikes = [
            scene.geometry.line(x0 - 0.03, y, x1 + 0.03, y)
            .stroke(BRICK, 0.016)
            .z_index(6)
            for x0, x1, y in before.spans
        ]
        progress = scene.geometry.line(-7.08, 1.59, -2.92, 1.59).stroke(STEEL, 0.03)
        scene.play(
            [
                sequence(
                    change.animate.fade_in().duration(0.1),
                    change.animate.move_along(loop).duration(0.9),
                    change.animate.fade_out().duration(0.1),
                    gap=0.01,
                ),
                ring.animate.rotate_by(2 * math.pi).duration(1.0).easing(Easing.SMOOTH),
                turns.count_to(n + 1, duration=0.5).delay(0.3),
                *[
                    c.animate.opacity(0.35).duration(0.3)
                    for c in before.pasted + [row[2] for row in before.rows]
                ],
                stagger(
                    *[st.animate.create().duration(0.2) for st in strikes], each=0.04
                ),
                *[
                    v.animate.opacity(0.2).duration(0.25).delay(0.85)
                    for v in etabs_ve[n - 1]
                ],
            ]
        )
        scene.play(
            [
                progress.animate.create().duration(0.6),
                stagger(
                    *[
                        parallel(
                            old.animate.fade_out().duration(0.15),
                            new.animate.fade_in().duration(0.2),
                        )
                        for old, new in zip(etabs_ve[n - 1], etabs_ve[n], strict=True)
                    ],
                    each=0.06,
                ).delay(0.5),
                progress.animate.fade_out().duration(0.2).delay(0.95),
            ]
        )
        # Cada valor tachado da paso al nuevo; la hoja recalcula Cumple después.
        row_strikes = [strikes[2 * i : 2 * i + 2] for i in range(len(before.rows))]
        sheet_strikes = strikes[2 * len(before.rows) :]
        scene.play(
            [
                _packets(scene, 10, *trip, each=0.1),
                stagger(
                    *[
                        parallel(
                            *[
                                x.animate.fade_out().duration(0.2)
                                for x in (*old, *marks)
                            ],
                            *[x.animate.fade_in().duration(0.2) for x in new[:2]],
                            new[2].animate.fade_in().duration(0.2).delay(0.2),
                        )
                        for old, marks, new in zip(
                            before.rows, row_strikes, after.rows, strict=True
                        )
                    ],
                    each=0.18,
                ).delay(0.6),
                stagger(
                    *[
                        parallel(
                            old.animate.fade_out().duration(0.2),
                            mark.animate.fade_out().duration(0.2),
                            new.animate.fade_in().duration(0.2),
                        )
                        for old, mark, new in zip(
                            before.sheet, sheet_strikes, after.sheet, strict=True
                        )
                    ],
                    each=0.3,
                ).delay(0.8),
            ]
        )
        scene.wait(0.6)  # tiempo para leer si X1 ya cumple
    takeaway_at(
        scene,
        "¿Cómo sistematizar la verificación de la norma E.070 a partir de un modelo de ETABS?",
    )
    source(
        scene,
        "Tesis · §1.1 Problemática y §1.2 Justificación, pp. 1–2. Valores: $V_e$ y $0.55 V_m$ del "
        "piso 1, MCT (Tabla 35, p. 86).",
    )
    scene.stop("pregunta-de-investigacion")


PASS_TINT = STEEL_SOFT
ETABS_ICON = ("E", "#2B6CB0")
EXCEL_ICON = ("X", "#107C41")
MATHCAD_ICON = ("M", "#5B4A8B")


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
        scene.geometry.line(close_x - g, bar_y - g, close_x + g, bar_y + g).stroke(
            INK_SOFT, 0.012
        ),
        scene.geometry.line(close_x - g, bar_y + g, close_x + g, bar_y - g).stroke(
            INK_SOFT, 0.012
        ),
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
                "1.25 min. (1) En ETABS, la lista de normas de diseño de muros es de concreto "
                "armado y extranjera (ACI, Eurocódigo, CSA, NZS...): la E.070 no está, ni ningún "
                "módulo de albañilería (§1.1). (2) Por eso el ingeniero exporta las tablas del "
                "modelo (fuerzas y propiedades de los Pier, derivas), filtra y copia a una hoja de "
                "cálculo o a Mathcad: 24 muros por 4 pisos, 96 filas por tabla y combinación. "
                "Riesgos citados en la tesis: errores de selección, transcripción, ordenamiento y "
                "verificaciones omitidas; no se midió su frecuencia. (3) En la hoja, X1 no cumple: "
                "se modifica el modelo, ETABS reanaliza, cambian los V_e de todos los muros y hay "
                "que volver a copiarlo todo; a la tercera vuelta cumple, con V_e y 0.55 V_m reales "
                "del piso 1 del modelo MCT (Tabla 35, p. 86). Cerrar con la pregunta de "
                "investigación."
            ),
        ),
    ],
)
