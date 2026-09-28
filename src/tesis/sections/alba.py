"""Bloque 6 · Implementación: arquitectura de Alba, API de ETABS, interfaz y reporte."""

from gaanim import (
    Anchor,
    Direction,
    Drawable,
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
from tesis.diagram import link
from tesis.kit import (
    LEFT_EDGE,
    RIGHT_EDGE,
    header,
    label,
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
    x0, w, h, gap, top = -2.55, 5.4, 0.6, 0.16, 2.3
    ys = [top - h / 2 - i * (h + gap) for i in range(len(MODULES))]
    boxes: list[Drawable] = []
    for i, ((name, tech), y) in enumerate(zip(MODULES, ys, strict=True)):
        core = i >= 2
        box = panel(
            scene,
            x0,
            y,
            w,
            h,
            fill=BRICK_SOFT if i == 4 else CARD,
            border=BRICK if i == 4 else RULE,
            anchor=Anchor.LEFT,
        )
        num = t(
            scene,
            f"{i + 1}",
            x0 + 0.25,
            y,
            font=DISPLAY,
            size=0.28,
            weight=700,
            color=BRICK if core else STEEL,
            anchor=Anchor.LEFT,
        )
        text = t(
            scene,
            name,
            x0 + 0.65,
            y,
            size=0.22,
            weight=700,
            color=INK,
            anchor=Anchor.LEFT,
        )
        tag = t(
            scene,
            tech,
            x0 + w - 0.2,
            y,
            font=MONO,
            size=0.14,
            color=MUTED,
            anchor=Anchor.RIGHT,
        )
        boxes.append(scene.geometry.group([box, num, text, tag]))
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
    takeaway(
        scene,
        "Cada diagrama de flujo del capítulo 6 es una rutina del módulo 5",
        y=-2.95,
    )
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
    left_col, mid, right_col = -6.2, -0.35, 0.35
    alba = pill(
        scene,
        "Alba · Python + comtypes",
        -3.4,
        2.35,
        font="Lato",
        weight=900,
        size=0.2,
        color=BRICK_DEEP,
        background=BRICK_SOFT,
    )
    etabs = pill(
        scene,
        "ETABS · SapModel",
        3.6,
        2.35,
        font="Lato",
        weight=900,
        size=0.2,
        color=STEEL,
        background=STEEL_SOFT,
    )
    scene.play(
        [alba.animate.fade_in().duration(0.3), etabs.animate.fade_in().duration(0.3)]
    )
    rules = [
        scene.geometry.line(LEFT_EDGE, y - 0.28, 7.3, y - 0.28).stroke("#E9E4DA", 0.008)
        for y in (1.72 - i * 0.56 for i in range(len(API_ROWS) - 1))
    ]
    # Cada fila es una consulta: el método se teclea, la flecha va a ETABS y
    # aparece lo que devuelve. Las filas se solapan como consultas seguidas.
    rows: list[Playable] = []
    for i, (cat, method, answer) in enumerate(API_ROWS):
        y = 1.72 - i * 0.56
        category = label(
            scene, cat, LEFT_EDGE, y, color=MUTED, size=0.12, anchor=Anchor.LEFT
        )
        call = t(
            scene,
            method,
            mid - 0.15,
            y,
            font=MONO,
            size=0.17,
            color=INK,
            anchor=Anchor.RIGHT,
        )
        arrow = link(scene, (mid, y), (right_col + 0.1, y), color=BRICK)
        reply = t(
            scene,
            answer,
            right_col + 0.3,
            y,
            size=0.21,
            color=INK_SOFT,
            anchor=Anchor.LEFT,
        )
        rows.append(
            sequence(
                parallel(
                    category.animate.fade_in().duration(0.2),
                    call.animate.typewriter(cps=60, cursor="▍", keep_cursor=False),
                ),
                parallel(
                    arrow.animate.grow_arrow().duration(0.25),
                    reply.animate.fade_in_from(Direction.LEFT, 0.08).duration(0.3),
                ),
            )
        )
    _ = left_col
    scene.play(
        [
            stagger(*[r.animate.fade_in().duration(0.3) for r in rules], each=0.04),
            stagger(*rows, each=0.35),
        ]
    )
    note = panel(
        scene,
        LEFT_EDGE,
        -2.75,
        14.6,
        0.62,
        fill=PAPER_DEEP,
        border=None,
        anchor=Anchor.LEFT,
    )
    note_t = t(
        scene,
        "Antes de leer: ¿hay una instancia abierta y el modelo está analizado? Si falta algo, "
        "la consola lo advierte y no se calcula.",
        LEFT_EDGE + 0.25,
        -2.75,
        size=0.2,
        color=INK,
        anchor=Anchor.LEFT,
    )
    scene.play(
        [note.animate.fade_in().duration(0.3), note_t.animate.fade_in().duration(0.4)]
    )
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
    width = 6.8
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
        fill="#FFFFFF",
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
        3.4,
        fill="#FFFFFF",
        border=RULE,
        anchor=Anchor.TOP_LEFT,
    )
    fragment = scene.media.image(
        thesis_image("cap7/resultado_typst.png"),
        width=7.0,
        height=3.0,
        fit="contain",
        quality="high",
    ).move_to(LEFT_EDGE + 3.7, 0.7)
    cap1 = t(
        scene,
        "Fragmento del PDF generado por Alba",
        LEFT_EDGE,
        -1.1,
        size=0.17,
        color=MUTED,
    )
    code_panel = panel(
        scene,
        0.55,
        2.4,
        6.75,
        3.4,
        fill="#23262E",
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
                    2.12 - i * 0.3,
                    font=MONO,
                    size=0.15,
                    color=color,
                )
            )
    cap2 = t(
        scene,
        "Plantilla Typst: los valores llegan desde un JSON",
        0.55,
        -1.1,
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

    steps = ["Python procesa", "resultados.json", "plantilla Typst", "PDF + Excel"]
    chain: list[Drawable] = []
    x = LEFT_EDGE
    for i, step in enumerate(steps):
        chip = pill(
            scene,
            step,
            x,
            -1.75,
            size=0.19,
            color=BRICK_DEEP if i == 3 else INK,
            background=BRICK_SOFT if i == 3 else PAPER_DEEP,
            anchor=Anchor.LEFT,
        )
        chain.append(chip)
        right = chip.bounds().right
        if i < len(steps) - 1:
            chain.append(
                link(scene, (right + 0.1, -1.75), (right + 0.5, -1.75), color=MUTED)
            )
        x = right + 0.63
    sections = [
        "Datos de diseño",
        "Requisitos mínimos",
        "Carga vertical",
        "Análisis sísmico",
        "Sismo moderado",
        "Información del modelo",
    ]
    sec_label = label(
        scene, "Secciones del reporte", LEFT_EDGE, -2.28, color=MUTED, size=0.13
    )
    chips: list[Drawable] = []
    x = LEFT_EDGE
    for name in sections:
        chips.append(
            pill(
                scene,
                name,
                x,
                -2.72,
                size=0.18,
                font="Lato",
                color=INK,
                background=CARD,
                border=RULE,
                anchor=Anchor.LEFT,
            )
        )
        x = chips[-1].bounds().right + 0.18
    scene.play(
        stagger(
            *[
                c.animate.fade_in_from(Direction.LEFT, 0.06).duration(0.3)
                for c in chain
            ],
            each=0.08,
        )
    )
    scene.play(
        [
            sec_label.animate.fade_in().duration(0.3),
            stagger(*[c.animate.fade_in().duration(0.25) for c in chips], each=0.06),
        ]
    )
    source(scene, "Tesis · Figuras 48 y 49, pp. 116–117; Tabla 48, p. 124")
    scene.stop("reporte-estructura")


SECTION = Section(
    "alba",
    [
        SectionStep(
            name="Alba · arquitectura",
            build=architecture,
            transition=Transition.cross_fade(0.45),
            notes=(
                "45 s. Seis módulos (cap. 7): interfaz (ImGui Bundle), gestión del proyecto (archivo "
                ".alb), conexión con ETABS por COM (comtypes), procesamiento (pandas: filtrar, "
                "clasificar por Pier y dirección), verificaciones normativas y visualización/reportes "
                "(Typst, openpyxl). El recorrido del punto sigue un dato desde ETABS hasta el PDF. "
                "Alba es de código libre."
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
                "45 s. Python procesa y exporta un JSON; la plantilla Typst compone el PDF con fórmulas, "
                "tablas, referencias normativas y capturas. El fragmento corresponde a la densidad "
                "mínima (0.032) del caso. Secciones según Tabla 48 (p. 124)."
            ),
        ),
    ],
)
