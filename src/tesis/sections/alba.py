"""Bloque 6 · Implementación: el programa Alba, su arquitectura, API de ETABS, interfaz
y reporte."""

import math
from typing import NamedTuple

from gaanim import (
    Anchor,
    Box,
    Color,
    Direction,
    Drawable,
    Easing,
    Playable,
    Scene,
    Section,
    SectionStep,
    Transition,
    parallel,
    sequence,
    stagger,
)

from tesis.app import thesis_image
from tesis.components import (
    chip,
    enter,
    fact,
    hairline,
    header,
    module_card,
    panel,
    source,
)
from tesis.components import page as page_column
from tesis.diagram import link
from tesis.kit import LEFT_EDGE, RIGHT_EDGE, t
from tesis.theme import (
    BRICK,
    BRICK_DEEP,
    BRICK_SOFT,
    DISPLAY,
    INK,
    INK_SOFT,
    MONO,
    MUTED,
    PAPER_DEEP,
    RULE,
    STEEL,
    STEEL_SOFT,
)

KICKER = "06 · Implementación: Alba"

# Ficha del programa (Tesis §7.1); versión y licencia salen del repositorio de Alba.
PROGRAM_FACTS = [
    ("Tipo", "Programa de escritorio"),
    ("Licencia", "Software libre"),
    ("Lenguaje", "Python"),
    ("Se conecta con", "ETABS por su API"),
]


def program(scene: Scene) -> None:
    header(scene, KICKER, "Alba es el programa de escritorio que implementa el marco")
    L = scene.layout
    # El ícono es el mismo del ejecutable; sus partes (tile, arc, pin, dot, arrow)
    # se arman una a una, como al abrir la aplicación.
    logo = scene.media.svg("alba-logo.svg").item(
        width="400px", height="400px", fit="contain"
    )
    wordmark = L.box("Alba", font=DISPLAY, font_size="150px", weight=700, color=INK)
    lead = L.box(
        "Verifica edificaciones de albañilería confinada\n"
        "a partir de su modelo analizado en ETABS",
        font_size="34px",
        color=INK_SOFT,
    )
    facts = L.column(
        *[
            L.row(
                *[fact(scene, name=n, value=v) for n, v in PROGRAM_FACTS[i : i + 2]],
                gap="48px",
                width="fill",
            )
            for i in (0, 2)
        ],
        gap="34px",
        width="fill",
    )
    info = L.column(wordmark, lead, facts, gap="36px", width="fill").item(grow=1)
    page_column(
        scene,
        body=[L.row(logo, info, gap="96px", align="center", width="fill")],
        justify="center",
    )
    scene.play(
        stagger(
            logo.part("tile").animate.fade_in_from(Direction.UP, 0.08).duration(0.45),
            parallel(
                logo.part("pin").animate.create().duration(0.9),
                logo.part("arc").animate.create().duration(0.7),
            ),
            logo.part("dot").animate.grow_from_center().duration(0.35),
            logo.part("arrow").animate.create().duration(0.4),
            each=0.3,
        )
    )
    scene.play(
        stagger(
            wordmark.animate.fade_in_from(Direction.LEFT, 0.08).duration(0.5),
            lead.animate.fade_in().duration(0.5),
            each=0.2,
        )
    )
    scene.stop("alba-programa")

    scene.play(enter(facts, each=0.08))
    source(
        scene,
        "Tesis · §7.1 Alcance de la implementación, p. 113 · Alba 0.1.0, licencia BSD-3-Clause",
    )
    scene.stop("alba-ficha")


MODULES = [
    ("Interfaz de usuario", "ImGui Bundle"),
    ("Gestión del proyecto", "configuración"),
    ("Conexión con ETABS · API COM", "comtypes"),
    ("Procesamiento de datos", "pandas"),
    ("Verificaciones normativas", "E.070 · E.030"),
    ("Visualización y reportes", "Typst · openpyxl"),
]


def architecture(scene: Scene) -> None:
    header(
        scene, KICKER, "Alba organiza el marco en seis módulos, del modelo al reporte"
    )
    x0, w, h, gap, top = -2.55, 5.4, 0.72, 0.27, 2.25
    cards = [
        module_card(
            scene,
            number=i + 1,
            name=name,
            tag=tech,
            core=i >= 2,
            highlight=i == 4,
            height=h,
        )
        for i, (name, tech) in enumerate(MODULES)
    ]
    scene.layout.column(
        *cards,
        gap=gap,
        within=scene.layout.safe.crop(top=top, left=x0, right=x0 + w),
        width="fill",
        height="fill",
        justify="start",
    )
    # Los módulos los coloca el layout; el resto del diagrama (llaves, flechas,
    # externos) se ancla a sus posiciones medidas.
    ys = [(c.bounds().top + c.bounds().bottom) / 2 for c in cards]
    boxes: list[Drawable] = list(cards)
    arrows = [
        link(
            scene, (x0 + 1.2, ys[i] - h / 2), (x0 + 1.2, ys[i + 1] + h / 2), color=MUTED
        )
        for i in range(len(ys) - 1)
    ]
    # Llaves: interacción con el usuario (1-2) y procesamiento interno (3-6).
    brackets: list[Drawable] = []
    for (a, b), name, color in [
        ((0, 1), "Interacción\ncon el usuario", STEEL),
        ((2, 5), "Procesamiento\ninterno", BRICK),
    ]:
        y_top, y_bot = ys[a] + h / 2, ys[b] - h / 2
        xb = x0 - 0.25
        brackets.append(
            scene.geometry.polyline(
                [(xb + 0.12, y_top), (xb, y_top), (xb, y_bot), (xb + 0.12, y_bot)]
            )
            .no_fill()
            .stroke(color, 0.018)
        )
        brackets.append(
            t(
                scene,
                name,
                xb - 0.15,
                (y_top + y_bot) / 2,
                size=0.18,
                weight=700,
                color=color,
                anchor=Anchor.RIGHT,
            )
        )
    scene.play(
        stagger(
            *[
                b.animate.fade_in_from(Direction.DOWN, 0.08).duration(0.35)
                for b in boxes
            ],
            each=0.1,
        )
    )
    scene.play(
        [
            *[a.animate.grow_arrow().duration(0.3) for a in arrows],
            *[b.animate.fade_in().duration(0.4) for b in brackets],
        ]
    )
    scene.stop("arquitectura-modulos")

    xr = 4.1
    externals = [
        (1, "Archivo del proyecto .alb", PAPER_DEEP, "↔"),
        (2, "Modelo analizado en ETABS", STEEL_SOFT, "→"),
        (4, "Capturas del modelo", PAPER_DEEP, "→"),
        (5, "Reporte PDF · tablas Excel", BRICK_SOFT, "←"),
    ]
    ext_items: list[Drawable] = []
    for index, name, fill, direction in externals:
        y = ys[index]
        ext_items.append(
            panel(scene, xr, y, 3.2, h, fill=fill, border=None, anchor=Anchor.LEFT)
        )
        ext_items.append(
            t(
                scene,
                name,
                xr + 1.6,
                y,
                size=0.19,
                weight=700,
                color=INK,
                anchor=Anchor.CENTER,
            )
        )
        start, end = (xr - 0.08, y), (x0 + w + 0.08, y)
        if direction == "←":
            start, end = end, start
        if index == 4:
            end = (x0 + w + 0.08, ys[5] + 0.12)
        ext_items.append(link(scene, start, end, color=INK_SOFT))
        if direction == "↔":
            ext_items.append(link(scene, end, start, color=INK_SOFT))
    scene.play(
        stagger(*[e.animate.fade_in().duration(0.3) for e in ext_items], each=0.05)
    )
    token = scene.geometry.circle(0.1).fill(BRICK).no_stroke().move_to(xr + 1.6, ys[2])
    scene.play(token.animate.fade_in().duration(0.2))
    path = [
        (x0 + w - 0.4, ys[2]),
        (x0 + w - 0.4, ys[3]),
        (x0 + w - 0.4, ys[4]),
        (x0 + w - 0.4, ys[5]),
        (xr + 1.6, ys[5]),
    ]
    scene.play(sequence(*[token.animate.move_to(x, y).duration(0.4) for x, y in path]))
    scene.play(token.animate.fade_out().duration(0.2))
    source(scene, "Tesis · Figura 50, p. 118 y Tabla 46, p. 115")
    scene.stop("arquitectura-flujo")


API_ROWS = [
    (
        "Niveles",
        "Story.Get_Stories_2 · Story.GetHeight",
        "nombres, elevaciones y alturas de entrepiso",
    ),
    ("Materiales", "PropMaterial.GetMPIsotropic", "módulo de elasticidad y de Poisson"),
    ("Muros", "PropArea.GetWall", "propiedades y espesores de muros"),
    (
        "Áreas",
        "AreaObj.GetPoints · GetDesignOrientation",
        "nodos, áreas y orientación de cada elemento",
    ),
    (
        "Frames",
        "FrameObj.GetSection · GetInsertionPoint_1",
        "secciones y puntos de inserción",
    ),
    ("Conectividad", "PointObj.GetConnectivity", "elementos conectados a cada nodo"),
    ("Tablas", "GetTableForDisplayArray", "tablas de resultados del análisis"),
    (
        "Control",
        "Analyze.RunAnalysis · GetModelIsLocked",
        "ejecución del análisis y bloqueo",
    ),
]


def api(scene: Scene) -> None:
    header(scene, KICKER, "Alba lee el modelo directamente mediante la API de ETABS")
    L = scene.layout
    cat_w, call_w, arrow_w = "230px", "640px", "150px"
    alba = chip(
        scene,
        text="Alba · Python + comtypes",
        color=BRICK_DEEP,
        background=BRICK_SOFT,
        font="Lato",
    )
    etabs = chip(
        scene, text="ETABS · SapModel", color=STEEL, background=STEEL_SOFT, font="Lato"
    )
    heading_row = L.row(
        L.box(width=cat_w).item(shrink=0),
        L.column(alba, width=call_w, align="end").item(shrink=0),
        L.box(width=arrow_w).item(shrink=0),
        etabs,
        gap="20px",
        align="center",
        width="fill",
    )
    # Cada fila es una consulta: el método se teclea, la flecha va a ETABS y
    # aparece lo que devuelve.
    call_rows = []
    for cat, method, answer in API_ROWS:
        call_rows.append(
            L.column(
                L.row(
                    L.box(
                        cat.upper(),
                        font_size="17px",
                        weight=900,
                        color=MUTED,
                        letter_spacing=0.03,
                        width=cat_w,
                    ).item(shrink=0),
                    L.box(
                        method,
                        font=MONO,
                        font_size="22px",
                        color=INK,
                        width=call_w,
                        align="end",
                    ).item(shrink=0),
                    scene.geometry.arrow(0, 0, 1.0, 0).fill(BRICK).no_stroke(),
                    L.box(answer, font_size="26px", color=INK_SOFT),
                    gap="20px",
                    align="center",
                    width="fill",
                ),
                hairline(scene, color="#E9E4DA"),
                gap="16px",
                width="fill",
            )
        )
    table = L.column(*call_rows, gap="22px", width="fill")
    closing = L.box(
        "Antes de leer: ¿hay una instancia abierta y el modelo está analizado? Si falta algo, "
        "la consola lo advierte y no se calcula.",
        font_size="26px",
        color=INK,
        background=PAPER_DEEP,
        padding=("16px", "26px"),
        width="fill",
    )
    page_column(scene, body=[heading_row, table, closing], gap="22px", top="190px")
    scene.play(enter(heading_row, each=0.1))
    plays: list[Playable] = []
    for row in call_rows:
        line = row.children[0]
        category, call, arrow, reply = line.children
        plays.append(
            sequence(
                parallel(
                    category.animate.fade_in().duration(0.2),
                    call.children[0].animate.typewriter(
                        cps=60, cursor="▍", keep_cursor=False
                    ),
                ),
                parallel(
                    arrow.animate.grow_arrow().duration(0.25),
                    reply.animate.fade_in_from(Direction.LEFT, 0.08).duration(0.3),
                ),
            )
        )
    rules = [row.children[1] for row in call_rows]
    scene.play(
        [
            stagger(*[r.animate.fade_in().duration(0.3) for r in rules], each=0.04),
            stagger(*plays, each=0.35),
        ]
    )
    scene.play(enter(closing))
    source(
        scene,
        "Tesis · Tabla 47, p. 120 · métodos tal como se listan en la tesis",
    )
    scene.stop("api-etabs")


# Zonas de ui_alba.png (1920 × 1032 px): (x0, y0, x1, y1) en píxeles.
UI_ZONES = [
    (
        (4, 24, 1048, 64),
        "Barra de herramientas",
        "importar desde ETABS, abrir y guardar\nel proyecto, generar reporte y Excel",
    ),
    (
        (8, 72, 340, 618),
        "Panel de flujo y estado",
        "conexión con ETABS, etapas del marco,\nalertas y modificaciones pendientes",
    ),
    (
        (350, 66, 1906, 858),
        "Panel de trabajo",
        "parámetros del proyecto, tablas de\nmuros y resultados con su estado",
    ),
    (
        (350, 862, 1906, 1022),
        "Consola de diagnósticos",
        "errores de conexión, datos faltantes\no inconsistentes en la importación",
    ),
]


def interface(scene: Scene) -> None:
    header(scene, KICKER, "La interfaz sigue las etapas del marco de trabajo")
    # La captura queda a la izquierda como mapa; a la derecha, una pantalla que toma
    # la proporción de cada zona la muestra entera.
    width = 4.6
    s = width / 1920
    height = 1032 * s
    x_left, y_top = LEFT_EDGE + 0.3, 2.5
    cx, cy = x_left + width / 2, y_top - height / 2
    frame = panel(
        scene,
        cx,
        cy,
        width + 0.12,
        height + 0.12,
        fill=Color.from_hex("#FFFFFF"),
        border=RULE,
    )
    shot = scene.media.image(
        thesis_image("cap7/ui_alba.png"),
        width=width,
        height=height,
        fit="contain",
        quality="high",
    ).move_to(cx, cy)
    scene.play(
        [frame.animate.fade_in().duration(0.4), shot.animate.fade_in().duration(0.6)]
    )

    def zone_box(i: int) -> tuple[float, float, float, float]:
        """Centro y tamaño de la zona i en coordenadas de escena."""
        px0, py0, px1, py1 = UI_ZONES[i][0]
        zx0, zx1 = x_left + px0 * s, x_left + px1 * s
        zy0, zy1 = y_top - py0 * s, y_top - py1 * s
        return (zx0 + zx1) / 2, (zy0 + zy1) / 2, zx1 - zx0, zy0 - zy1

    # Caja libre a la derecha: la pantalla crece hasta llenarla por el lado que
    # limite y queda a la altura de su zona mientras quepa.
    bx0, bx1, by0, by1 = x_left + width + 0.5, RIGHT_EDGE, y_top, -3.2

    def screen_box(i: int) -> tuple[float, float, float, float]:
        _, zy, zw, zh = zone_box(i)
        k = min((bx1 - bx0) / zw, (by0 - by1) / zh)
        w, h = zw * k, zh * k
        return (bx0 + bx1) / 2, min(max(zy, by1 + h / 2), by0 - h / 2), w, h

    def legend_item(i: int, x: float, y: float) -> list[Drawable]:
        _, name, body = UI_ZONES[i]
        return [
            t(
                scene,
                f"{i + 1}",
                x,
                y,
                font=DISPLAY,
                size=0.36,
                weight=700,
                color=BRICK,
            ),
            t(scene, name, x + 0.45, y + 0.02, size=0.23, weight=900, color=INK),
            t(scene, body, x + 0.45, y - 0.32, size=0.18, color=INK_SOFT),
        ]

    outlines: list[Drawable] = []
    numerals: list[Drawable] = []
    for i in range(len(UI_ZONES)):
        zx, zy, zw, zh = zone_box(i)
        outlines.append(
            scene.geometry.rect(zw, zh).no_fill().stroke(BRICK, 0.03).move_to(zx, zy)
        )
        # Numerales sin superponerse: 1 al final de la barra, 2 fuera a la izquierda, 3 y 4 dentro.
        nx, ny = [
            (zx + zw / 2 + 0.2, zy),
            (zx - zw / 2 - 0.2, zy),
            (zx + zw / 2 - 0.25, zy + zh / 2 - 0.25),
            (zx + zw / 2 - 0.25, zy + zh / 2 - 0.25),
        ][i]
        numerals.append(
            t(
                scene,
                str(i + 1),
                nx,
                ny,
                font=DISPLAY,
                size=0.32,
                weight=700,
                color=BRICK,
                anchor=Anchor.CENTER,
            )
        )

    # La cámara es un rectángulo invisible que se estira sobre cada zona y la
    # pantalla se estira igual, así que la zona entra entera y sin deformarse.
    zx, zy, zw, zh = zone_box(0)
    sx, sy, sw, sh = screen_box(0)
    lens = (
        scene.geometry.rect(1, 1)
        .no_fill()
        .no_stroke()
        .move_to(zx, zy)
        .scale_to_3d(zw, zh, 1)
    )
    screen = (
        scene.geometry.rect(1, 1)
        .fill("#FFFFFF")
        .stroke(INK_SOFT, 0.02)
        .move_to(sx, sy)
        .scale_to_3d(sw, sh, 1)
    )
    screen.camera_view(lens, exclude=[*outlines, *numerals])

    current: list[Drawable] = []
    for i in range(len(UI_ZONES)):
        zx, zy, zw, zh = zone_box(i)
        sx, sy, sw, sh = screen_box(i)
        if i == 0:
            view = [screen.animate.fade_in().duration(0.6)]
        else:
            view = [
                lens.animate.move_to(zx, zy).scale_to_3d(zw, zh, 1).duration(0.8),
                screen.animate.move_to(sx, sy).scale_to_3d(sw, sh, 1).duration(0.8),
            ]
        item = legend_item(i, x_left, y_top - height - 0.45)
        scene.play(
            [
                outlines[i].animate.create().duration(0.5),
                numerals[i].animate.fade_in().duration(0.3).delay(0.2),
                *view,
                *[c.animate.fade_out().duration(0.25) for c in current],
                stagger(
                    *[c.animate.fade_in().duration(0.3) for c in item], each=0.06
                ).delay(0.4),
            ]
        )
        current = item
        if i < len(UI_ZONES) - 1:
            scene.stop(f"interfaz-zona-{i + 1}")

    # Cierre: la pantalla se retira y queda la leyenda completa a la derecha.
    legend = [
        c for i in range(len(UI_ZONES)) for c in legend_item(i, bx0, 2.2 - i * 1.25)
    ]
    scene.play(
        [
            screen.animate.fade_out().duration(0.4),
            *[c.animate.fade_out().duration(0.25) for c in current],
            stagger(
                *[c.animate.fade_in().duration(0.25) for c in legend], each=0.04
            ).delay(0.4),
        ]
    )
    source(
        scene,
        "Tesis · Figura 51, p. 121 · captura de Alba v0.1.0 con el modelo del caso (ModeloBartolomes.EDB)",
    )
    scene.stop("interfaz")


REPORT_CODE = """// Importación de resultados
#let datos = json("resultados.json")

== Densidad mínima de muros #e070_badge("Art 19.2 (b)")

$ frac(sum L dot t, A_p) gt.eq
  frac(#datos.f_zona dot #datos.f_uso dot
       #datos.f_suelo dot #datos.niveles, 56)
  = #datos.den_min_norm $"""


def report(scene: Scene) -> None:
    header(scene, KICKER, "El reporte documenta cada iteración con fórmulas y valores")
    page = panel(
        scene,
        LEFT_EDGE,
        2.4,
        7.4,
        3.9,
        fill=Color.from_hex("#FFFFFF"),
        border=RULE,
        anchor=Anchor.TOP_LEFT,
    )
    fragment = scene.media.image(
        thesis_image("cap7/resultado_typst.png"),
        width=7.0,
        height=3.5,
        fit="contain",
        quality="high",
    ).move_to(LEFT_EDGE + 3.7, 0.45)
    cap1 = t(
        scene,
        "Fragmento del PDF generado por Alba",
        LEFT_EDGE,
        -1.6,
        size=0.17,
        color=MUTED,
    )
    code_panel = panel(
        scene,
        0.55,
        2.4,
        6.75,
        3.9,
        fill=Color.from_hex("#23262E"),
        border=None,
        anchor=Anchor.TOP_LEFT,
    )
    code_lines = REPORT_CODE.split("\n")
    code: list[Drawable] = []
    for i, line in enumerate(code_lines):
        color = (
            "#8C93A3"
            if line.startswith("//")
            else ("#E9B48F" if line.startswith("==") else "#E6E3DC")
        )
        if line.strip():
            code.append(
                t(
                    scene,
                    line.replace("$", "\\$"),
                    0.8,
                    2.1 - i * 0.36,
                    font=MONO,
                    size=0.17,
                    color=color,
                )
            )
    cap2 = t(
        scene,
        "Plantilla Typst: los valores llegan desde un JSON",
        0.55,
        -1.6,
        size=0.17,
        color=MUTED,
    )
    scene.play(
        [
            page.animate.fade_in().duration(0.3),
            fragment.animate.fade_in().duration(0.6),
            cap1.animate.fade_in().duration(0.4),
        ]
    )
    scene.play(
        [
            code_panel.animate.fade_in().duration(0.3),
            stagger(*[c.animate.fade_in().duration(0.2) for c in code], each=0.05),
            cap2.animate.fade_in().duration(0.4),
        ]
    )
    scene.stop("reporte-fragmento")

    L = scene.layout
    steps = ["Python procesa", "resultados.json", "plantilla Typst", "PDF + Excel"]
    chain_items: list[Drawable] = []
    for i, step in enumerate(steps):
        last = i == len(steps) - 1
        chain_items.append(
            chip(
                scene,
                text=step,
                color=BRICK_DEEP if last else INK,
                background=BRICK_SOFT if last else PAPER_DEEP,
            )
        )
        if not last:
            chain_items.append(
                scene.geometry.arrow(0, 0, 0.4, 0).fill(MUTED).no_stroke()
            )
    chain = L.row(*chain_items, gap="16px", align="center", width="fill")
    page_column(scene, body=[chain], top="790px")
    scene.play(enter(chain, each=0.08, duration=0.3))
    source(scene, "Tesis · Figuras 48 y 49, pp. 116–117")
    scene.stop("reporte-cadena")


class ReportPart(NamedTuple):
    pages: tuple[int, int]  # primera y última página del PDF, desde 1
    name: str  # título de la sección en el reporte
    content: str  # Tabla 48
    cites: str  # normas citadas en sus páginas o, en la última, sus datos
    read: int  # página que se lee en la diapositiva
    region: tuple[float, float, float, float]  # x0, y0, x1, y1 en puntos del PDF


# Reporte del caso (anexo de la tesis, 21 páginas A4): portada e índice y seis partes.
# Las páginas salen de tools/render_report.py: miniaturas para la tira y, a 200 dpi,
# la portada y las páginas que se leen.
REPORT_PAGES = 21
PAGE_PT = (595.28, 841.89)
COVER_REGION = (0, 95, 595, 575)
REPORT_PARTS = [
    ReportPart(
        (3, 5),
        "Datos de diseño",
        "Geometría, niveles, materiales y parámetros sísmicos",
        "E.020 · E.030 · E.070",
        3,
        (48, 58, 548, 308),
    ),
    ReportPart(
        (6, 7),
        "Requisitos estructurales mínimos",
        "Espesor efectivo y densidad mínima de muros en cada dirección",
        "E.070 Art. 19.1 (a) · Art. 19.2 (b)",
        6,
        (44, 90, 556, 352),
    ),
    ReportPart(
        (8, 10),
        "Análisis por carga vertical",
        "Esfuerzo axial por cargas de gravedad, muro por muro",
        "E.070 Art. 19.1 (b)",
        8,
        (48, 88, 548, 338),
    ),
    ReportPart(
        (11, 14),
        "Análisis sísmico",
        "Peso sísmico, modos, fuerzas equivalentes y derivas",
        "E.030 Art. 18, 31, 33–35, 40, 50 y 51",
        14,
        (48, 50, 548, 300),
    ),
    ReportPart(
        (15, 20),
        "Análisis elástico para sismo moderado",
        "Control de fisuración y resistencia al corte global, muro por muro",
        "E.070 Art. 22 (b), 26.2–26.4",
        15,
        (48, 88, 548, 338),
    ),
    ReportPart(
        (21, 21),
        "Información del modelo y del reporte",
        "Versión de la API, modelo, fecha de importación y archivo",
        "API 22.6.0 · ModeloBartolomes.EDB · Alba 0.1.0",
        21,
        (48, 55, 548, 215),
    ),
]
DIM = 0.3  # opacidad de lo que no es la parte en lectura


def report_parts(scene: Scene) -> None:
    header(scene, KICKER, "El reporte del caso reúne seis partes en 21 páginas")
    # Arriba, el documento entero: sus 21 páginas en una tira, agrupadas por parte.
    groups = [(1, 2), *[part.pages for part in REPORT_PARTS]]
    inner, outer, top = 0.05, 0.26, 2.42
    inner_gaps = sum(last - first for first, last in groups)
    tw = (
        RIGHT_EDGE - LEFT_EDGE - inner * inner_gaps - outer * (len(groups) - 1)
    ) / REPORT_PAGES
    th = tw * PAGE_PT[1] / PAGE_PT[0]
    slots: dict[int, tuple[float, float]] = {}
    thumbs: dict[int, Drawable] = {}
    x = LEFT_EDGE
    for g, (first, last) in enumerate(groups):
        x += outer - inner if g else 0
        for n in range(first, last + 1):
            slots[n] = (x + tw / 2, top - th / 2)
            thumbs[n] = scene.geometry.group(
                scene.media.image(
                    f"reporte/miniaturas/p{n:02}.png",
                    width=tw,
                    height=th,
                    quality="high",
                ),
                scene.geometry.rect(tw, th).no_fill().stroke(RULE, 0.012),
            ).move_to(*slots[n])
            x += tw + inner
    marks: list[Drawable] = []
    yb = top - th - 0.1
    for i, part in enumerate(REPORT_PARTS):
        first, last = part.pages
        x0, x1 = slots[first][0] - tw / 2, slots[last][0] + tw / 2
        marks.append(
            scene.geometry.group(
                scene.geometry.polyline(
                    [(x0, yb + 0.06), (x0, yb), (x1, yb), (x1, yb + 0.06)]
                )
                .no_fill()
                .stroke(MUTED, 0.016),
                t(
                    scene,
                    f"{i + 1}",
                    (x0 + x1) / 2,
                    yb - 0.07,
                    font=DISPLAY,
                    size=0.24,
                    weight=700,
                    color=BRICK,
                    anchor=Anchor.TOP,
                ),
            )
        )

    # Abajo a la izquierda, el índice: cada parte se despliega cuando se lee.
    L = scene.layout
    bottom = 0.95
    entries = []
    for i, part in enumerate(REPORT_PARTS):
        first, last = part.pages
        entries.append(
            L.column(
                L.row(
                    L.box(
                        f"{i + 1}",
                        font=DISPLAY,
                        font_size="30px",
                        weight=700,
                        color=BRICK,
                        width="34px",
                    ).item(shrink=0),
                    L.box(part.name, font_size="25px", weight=900, color=INK).item(
                        grow=1
                    ),
                    L.box(
                        f"p. {first}" if first == last else f"pp. {first}–{last}",
                        font=MONO,
                        font_size="18px",
                        color=MUTED,
                    ).item(shrink=0),
                    gap="14px",
                    align="center",
                    width="fill",
                ),
                hairline(scene, color="#E9E4DA"),
                gap="12px",
                width="fill",
            )
        )
    reader_left = -1.1
    # El índice empieza bajo la tira, a y = bottom.
    L.column(
        *entries,
        gap="12px",
        within=L.safe.crop(top=bottom, left=LEFT_EDGE, right=reader_left - 0.4),
        width="fill",
        height="fill",
        justify="start",
    )

    def detail(part: ReportPart) -> Box:
        return L.column(
            L.box(part.content, font_size="22px", color=INK_SOFT),
            L.box(part.cites, font=MONO, font_size="17px", color=MUTED),
            gap="6px",
            width="fill",
            padding=("0px", "0px", "4px", "48px"),
        )

    # A la derecha, el lector: la página sale de su lugar en la tira y se acerca
    # hasta la región que se lee. Viaja en arco por la franja de la tira y crece al
    # final del viaje, para no cruzar el índice.
    rw, rh = RIGHT_EDGE - reader_left, bottom + 3.38
    rc = (reader_left + rw / 2, bottom - rh / 2)
    sheet = panel(scene, *rc, rw, rh, fill=Color.from_hex("#FFFFFF"), border=RULE)

    def lift(n: int, region: tuple[float, float, float, float]):
        w, h = rw - 0.24, rh - 0.24
        page = (
            scene.media.image(
                f"reporte/paginas/p{n:02}.png",
                width=w,
                height=h,
                fit="contain",
                quality="high",
            )
            .scale_to(th / h)
            .move_to(*slots[n])
        )
        x0, y0, x1, y1 = region
        pw, ph = PAGE_PT
        crop = (x0 / pw, y0 / ph, (x1 - x0) / pw, (y1 - y0) / ph)
        reach = (rc[0] - slots[n][0]) / (rc[0] - LEFT_EDGE)
        return page, [
            page.animate.fade_in().duration(0.35),
            page.animate.move_to(*rc)
            .path_arc(-math.pi / 3 * reach)
            .duration(0.9)
            .easing(Easing.SMOOTH),
            page.animate.scale_to(1)
            .crop(*crop, normalized=True)
            .duration(0.75)
            .delay(0.25)
            .easing(Easing.SMOOTH),
        ]

    reveals: list[Playable] = [
        stagger(
            *[
                thumbs[n].animate.fade_in_from(Direction.DOWN, 0.06).duration(0.3)
                for n in range(1, 3)
            ],
            each=0.04,
        )
    ]
    for i, part in enumerate(REPORT_PARTS):
        first, last = part.pages
        reveals.append(
            parallel(
                stagger(
                    *[
                        thumbs[n]
                        .animate.fade_in_from(Direction.DOWN, 0.06)
                        .duration(0.3)
                        for n in range(first, last + 1)
                    ],
                    each=0.04,
                ),
                marks[i].animate.fade_in().duration(0.35),
                entries[i].animate.fade_in_from(Direction.LEFT, 0.06).duration(0.35),
            )
        )
    scene.play(stagger(*reveals, each=0.16))
    current, flight = lift(1, COVER_REGION)
    scene.play([sheet.animate.fade_in().duration(0.3), *flight])
    source(
        scene,
        "Tesis · Anexo: reporte automatizado del modelo ejemplo · estructura de la Tabla 48, p. 124",
    )
    scene.stop("reporte-partes")

    shown: Box | None = None
    for i, part in enumerate(REPORT_PARTS):
        first, last = part.pages
        # El detalle de la parte anterior se pliega mientras el nuevo se despliega.
        if shown is not None:
            entries[i - 1].remove(shown, duration=0.45, advance=False, exit="fold")
        shown = detail(part)
        entries[i].add(shown, at=1, duration=0.45, advance=False, enter="unfold")
        page, flight = lift(part.read, part.region)
        scene.play(
            [
                *[
                    thumb.animate.opacity(1 if first <= n <= last else DIM).duration(
                        0.4
                    )
                    for n, thumb in thumbs.items()
                ],
                *[
                    m.animate.opacity(1 if j == i else DIM).duration(0.4)
                    for j, m in enumerate(marks)
                ],
                *[
                    e.animate.opacity(1 if j == i else 0.45).duration(0.4)
                    for j, e in enumerate(entries)
                ],
                current.animate.fade_out().duration(0.3),
                *flight,
            ]
        )
        current = page
        scene.stop(f"reporte-parte-{i + 1}")


SECTION = Section(
    "alba",
    [
        SectionStep(
            name="Alba · el programa",
            build=program,
            transition=Transition.cross_fade(0.45),
            notes=(
                "30 s. Presentar Alba como software antes de su arquitectura: programa de "
                "escritorio de desarrollo propio (§7.1, p. 113) que lee un modelo analizado en "
                "ETABS por su API, ejecuta las verificaciones de la E.070 y la E.030 y genera el "
                "reporte. Escrito en Python; software libre (licencia BSD-3-Clause, versión 0.1.0)."
            ),
        ),
        SectionStep(
            name="Alba · arquitectura",
            build=architecture,
            transition=Transition.cross_fade(0.45),
            notes=(
                "45 s. Seis módulos (cap. 7): interfaz (ImGui Bundle), gestión del proyecto (archivo "
                ".alb), conexión con ETABS por COM (comtypes), procesamiento (pandas: filtrar, "
                "clasificar por Pier y dirección), verificaciones normativas y visualización/reportes "
                "(Typst, openpyxl). El recorrido del punto sigue un dato desde ETABS hasta el PDF. "
                "Alba es software libre."
            ),
        ),
        SectionStep(
            name="Alba · API de ETABS",
            build=api,
            transition=Transition.cross_fade(0.45),
            notes=(
                "45 s. Tabla 47 (p. 120): métodos consultados para niveles, materiales, muros, "
                "elementos de área y frame, conectividad, tablas de resultados y control del análisis. "
                "Esto reemplaza la exportación manual de tablas. Antes de leer se comprueba que exista "
                "una instancia abierta y un modelo analizado; si no, la consola advierte."
            ),
        ),
        SectionStep(
            name="Alba · interfaz",
            build=interface,
            transition=Transition.cross_fade(0.45),
            notes=(
                "45 s. Captura real (Figura 51 (p. 121)) con el modelo del caso: 136.51 m², 4 pisos, zona 4. "
                "Barra de herramientas; panel de flujo con estado de conexión y etapas (proyecto, muros, "
                "verificaciones, capturas, reporte); panel de trabajo; consola de diagnósticos. No es una "
                "demostración en vivo."
            ),
        ),
        SectionStep(
            name="Alba · reporte",
            build=report,
            transition=Transition.cross_fade(0.45),
            notes=(
                "30 s. Python procesa y exporta un JSON; la plantilla Typst compone el PDF con fórmulas, "
                "tablas, referencias normativas y capturas. El fragmento corresponde a la densidad "
                "mínima (0.032) del caso."
            ),
        ),
        SectionStep(
            name="Alba · partes del reporte",
            build=report_parts,
            transition=Transition.cross_fade(0.45),
            notes=(
                "30 s. El reporte real del caso (anexo, 21 páginas): arriba sus páginas, agrupadas "
                "en las seis secciones de la Tabla 48 (p. 124); cada pausa abre una en el índice y "
                "acerca una página. 1 Datos de diseño (pp. 3–5). 2 Requisitos mínimos: espesor "
                "t = 0.12 m y densidad mínima 0.032 (pp. 6–7). 3 Carga vertical: esfuerzo axial "
                "muro por muro (pp. 8–10). 4 Análisis sísmico: peso, modos, fuerzas y derivas; la "
                "página muestra la deriva en X (pp. 11–14). 5 Sismo moderado: fisuración y corte "
                "global, la parte más larga (pp. 15–20). 6 Información del modelo: versión de la "
                "API, archivo y fecha de importación, la trazabilidad de la iteración (p. 21)."
            ),
        ),
    ],
)
