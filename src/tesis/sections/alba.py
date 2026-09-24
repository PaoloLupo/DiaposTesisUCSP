"""Bloque 6 · Implementación: arquitectura de Alba, API de ETABS, interfaz y reporte."""

from gaanim import (
    Anchor,
    Direction,
    Drawable,
    Scene,
    Section,
    SectionStep,
    Transition,
    sequence,
    stagger,
)

from tesis.app import thesis_image
from tesis.diagram import link
from tesis.kit import LEFT_EDGE, header, label, panel, pill, source, t, takeaway
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
    rows: list[Drawable] = []
    for i, (cat, method, answer) in enumerate(API_ROWS):
        y = 1.72 - i * 0.56
        rows.append(
            scene.geometry.group(
                [
                    label(
                        scene,
                        cat,
                        LEFT_EDGE,
                        y,
                        color=MUTED,
                        size=0.12,
                        anchor=Anchor.LEFT,
                    ),
                    t(
                        scene,
                        method,
                        mid - 0.15,
                        y,
                        font=MONO,
                        size=0.17,
                        color=INK,
                        anchor=Anchor.RIGHT,
                    ),
                    link(scene, (mid, y), (right_col + 0.1, y), color=BRICK),
                    t(
                        scene,
                        answer,
                        right_col + 0.3,
                        y,
                        size=0.21,
                        color=INK_SOFT,
                        anchor=Anchor.LEFT,
                    ),
                ]
            )
        )
        if i < len(API_ROWS) - 1:
            rows.append(
                scene.geometry.line(LEFT_EDGE, y - 0.28, 7.3, y - 0.28).stroke(
                    "#E9E4DA", 0.008
                )
            )
    _ = left_col
    scene.play(
        stagger(
            *[r.animate.fade_in_from(Direction.LEFT, 0.08).duration(0.3) for r in rows],
            each=0.08,
        )
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
    width = 10.4
    cx, cy = -1.75, -0.35
    s = width / 1920
    height = 1032 * s
    x_left, y_top = cx - width / 2, cy + height / 2
    frame = panel(
        scene,
        cx,
        cy,
        width + 0.12,
        height + 0.12,
        fill="#FFFFFF",
        border=RULE,
        radius=0.06,
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
    legend_x = 3.95
    for i, ((px0, py0, px1, py1), name, body) in enumerate(UI_ZONES):
        zx0, zx1 = x_left + px0 * s, x_left + px1 * s
        zy0, zy1 = y_top - py0 * s, y_top - py1 * s
        outline = (
            scene.geometry.rounded_rect(zx1 - zx0, zy0 - zy1, 0.05)
            .no_fill()
            .stroke(BRICK, 0.03)
            .move_to((zx0 + zx1) / 2, (zy0 + zy1) / 2)
        )
        # Insignias sin superponerse: 1 al final de la barra, 2 fuera a la izquierda, 3 y 4 dentro.
        bx, by = [
            (zx1 + 0.25, (zy0 + zy1) / 2),
            (zx0 - 0.25, (zy0 + zy1) / 2),
            (zx1 - 0.3, zy0 - 0.3),
            (zx1 - 0.3, zy0 - 0.3),
        ][i]
        badge = scene.geometry.circle(0.17).fill(BRICK).no_stroke().move_to(bx, by)
        badge_n = t(
            scene,
            str(i + 1),
            bx,
            by,
            size=0.2,
            weight=900,
            color="#FFFFFF",
            anchor=Anchor.CENTER,
        )
        y = 2.2 - i * 1.25
        item_n = t(
            scene,
            f"{i + 1}",
            legend_x,
            y,
            font=DISPLAY,
            size=0.36,
            weight=700,
            color=BRICK,
        )
        item_t = t(
            scene, name, legend_x + 0.45, y + 0.02, size=0.23, weight=900, color=INK
        )
        item_b = t(scene, body, legend_x + 0.45, y - 0.32, size=0.18, color=INK_SOFT)
        scene.play(
            stagger(
                outline.animate.create().duration(0.5),
                badge.animate.grow_from_center().duration(0.25),
                badge_n.animate.fade_in().duration(0.2),
                stagger(
                    item_n.animate.fade_in().duration(0.3),
                    item_t.animate.fade_in().duration(0.3),
                    item_b.animate.fade_in().duration(0.3),
                    each=0.06,
                ),
                each=0.12,
            )
        )
        if i < len(UI_ZONES) - 1:
            scene.stop(f"interfaz-zona-{i + 1}")
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
        radius=0.06,
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
        radius=0.1,
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
        w_, _ = scene.text.measure(step, size=0.19, font=MONO)
        chain.append(
            pill(
                scene,
                step,
                x,
                -1.75,
                size=0.19,
                color=BRICK_DEEP if i == 3 else INK,
                background=BRICK_SOFT if i == 3 else PAPER_DEEP,
                anchor=Anchor.LEFT,
            )
        )
        if i < len(steps) - 1:
            chain.append(
                link(scene, (x + w_ + 0.42, -1.75), (x + w_ + 0.82, -1.75), color=MUTED)
            )
        x += w_ + 0.95
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
        w_, _ = scene.text.measure(name, size=0.18, font="Lato")
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
        x += w_ + 0.5
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
    source(
        scene, "Tesis · Figuras 48 y 49, pp. 116–117; Tabla 48, p. 124"
    )
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
