"""Bloque 2 · Objetivos, hipótesis y método de la investigación."""

from gaanim import (
    Anchor,
    Direction,
    Drawable,
    Scene,
    Section,
    SectionStep,
    Transition,
    stagger,
)

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

KICKER = "02 · Objetivos y método"


def purpose(scene: Scene) -> None:
    header(scene, KICKER, "Un marco de trabajo entre ETABS y la verificación E.070")

    tag = label(scene, "Objetivo general", LEFT_EDGE, 2.35, color=BRICK)
    objective = t(
        scene,
        "Desarrollar un marco de trabajo para la\n"
        "automatización de la verificación normativa\n"
        "de la distribución de muros en planta de\n"
        "edificios de albañilería confinada (E.070),\n"
        "aplicado en un programa propio que\n"
        "interactúa con el software ETABS.",
        LEFT_EDGE,
        2.0,
        font=DISPLAY,
        size=0.36,
        weight=400,
        color=INK,
    )
    scene.play(
        stagger(
            tag.animate.fade_in().duration(0.3),
            objective.animate.fade_in_from(Direction.UP, 0.1).duration(0.8),
            each=0.15,
        )
    )

    chain = [
        ("ETABS", "modelo analizado"),
        ("Marco", "procesos y flujos"),
        ("Alba", "programa propio"),
        ("Reporte", "memoria trazable"),
    ]
    nodes: list[Drawable] = []
    for i, (name, sub) in enumerate(chain):
        x = LEFT_EDGE + 0.85 + i * 2.25
        box = panel(
            scene,
            x,
            -1.85,
            1.75,
            0.9,
            fill=BRICK_SOFT if name in ("Marco", "Alba") else CARD,
            border=None if name in ("Marco", "Alba") else RULE,
        )
        nodes.append(box)
        nodes.append(
            t(
                scene,
                name,
                x,
                -1.72,
                size=0.24,
                weight=900,
                color=BRICK_DEEP if name in ("Marco", "Alba") else INK,
                anchor=Anchor.CENTER,
            )
        )
        nodes.append(
            t(scene, sub, x, -2.05, size=0.15, color=INK_SOFT, anchor=Anchor.CENTER)
        )
        if i:
            nodes.append(
                scene.geometry.arrow(
                    x - 1.37,
                    -1.85,
                    x - 0.93,
                    -1.85,
                    head_length=0.12,
                    head_width=0.12,
                    body_width=0.022,
                )
                .fill(MUTED)
                .no_stroke()
            )
    scene.play(stagger(*[n.animate.fade_in().duration(0.3) for n in nodes], each=0.05))
    scene.stop("objetivo-general")

    card = panel(scene, 2.35, 2.45, 4.95, 4.95, fill=CARD, anchor=Anchor.TOP_LEFT)
    h_badge = scene.geometry.circle(0.26).fill(STEEL).no_stroke().move_to(2.9, 1.95)
    h_letter = t(
        scene,
        "H",
        2.9,
        1.95,
        font=DISPLAY,
        size=0.3,
        weight=700,
        color="#FFFFFF",
        anchor=Anchor.CENTER,
    )
    h_tag = label(scene, "Hipótesis", 3.35, 2.05, color=STEEL)
    hypothesis = t(
        scene,
        "Un marco automatizado, integrado a ETABS\n"
        "mediante su API, permitirá sistematizar\n"
        "la extracción y el procesamiento de datos\n"
        "del modelo de elementos finitos, así como\n"
        "ejecutar y documentar las verificaciones\n"
        "normativas.",
        2.7,
        1.45,
        size=0.23,
        color=INK,
    )
    rule = scene.geometry.line(2.7, -0.35, 6.95, -0.35).stroke(RULE, 0.012)
    variables = [
        (
            "Variable independiente",
            "Método de verificación:\nmanual o automatizado",
            -0.55,
        ),
        ("Variable dependiente", "Cumplimiento normativo", -1.55),
    ]
    var_items: list[Drawable] = []
    for name, body, y in variables:
        var_items.append(label(scene, name, 2.7, y, color=MUTED, size=0.13))
        var_items.append(
            t(scene, body, 2.7, y - 0.25, size=0.22, weight=700, color=INK)
        )
    scene.play(
        stagger(
            card.animate.fade_in().duration(0.4),
            h_badge.animate.grow_from_center().duration(0.3),
            h_letter.animate.fade_in().duration(0.2),
            h_tag.animate.fade_in().duration(0.3),
            hypothesis.animate.fade_in().duration(0.6),
            rule.animate.create().duration(0.4),
            *[v.animate.fade_in().duration(0.3) for v in var_items],
            each=0.1,
        )
    )
    source(
        scene,
        "Tesis · cap. 1, Objetivo general, Hipótesis y Variables de la investigación",
    )
    scene.stop("hipotesis")


SPECIFIC = [
    (
        "Identificar",
        "el proceso manual de\ndiseño de la distribución\nde muros con un software\nde elementos finitos y\nhojas de cálculo.",
        "Flujo manual · cap. 5",
    ),
    (
        "Desarrollar",
        "un marco de trabajo para\nautomatizar la verificación,\na partir de actividades\ncríticas y repetitivas,\ncon diagramas de flujo.",
        "Diagramas · cap. 6",
    ),
    (
        "Aplicar",
        "el marco en un programa\nque interactúa con ETABS\nmediante su interfaz de\nprogramación (API).",
        "Alba + API · cap. 7",
    ),
    (
        "Evaluar",
        "los resultados del caso\ncomparando alternativas\nde modelamiento y la\nverificación normativa.",
        "Comparación · cap. 8",
    ),
]


def specific(scene: Scene) -> None:
    header(scene, KICKER, "Cuatro objetivos específicos, cuatro productos")
    w, gap = 3.45, 0.27
    items: list[list[Drawable]] = []
    for i, (verb, body, product) in enumerate(SPECIFIC):
        x0 = LEFT_EDGE + i * (w + gap)
        card = panel(scene, x0, 2.35, w, 4.15, fill=CARD, anchor=Anchor.TOP_LEFT)
        number = t(
            scene,
            f"{i + 1}",
            x0 + 0.3,
            2.15,
            font=DISPLAY,
            size=0.9,
            weight=700,
            color=BRICK,
        )
        verb_t = t(scene, verb, x0 + 0.3, 0.95, size=0.36, weight=900, color=INK)
        body_t = t(scene, body, x0 + 0.3, 0.4, size=0.235, color=INK_SOFT)
        tag = pill(
            scene,
            product,
            x0 + 0.3,
            -1.45,
            color=BRICK_DEEP,
            background=BRICK_SOFT,
            size=0.15,
            anchor=Anchor.LEFT,
        )
        items.append([card, number, verb_t, body_t, tag])
    for group in items:
        scene.play(
            stagger(
                *[
                    g.animate.fade_in_from(Direction.UP, 0.08).duration(0.4)
                    for g in group
                ],
                each=0.06,
            )
        )
    flow = (
        scene.geometry.arrow(
            LEFT_EDGE + 0.3,
            -2.2,
            7.0,
            -2.2,
            head_length=0.16,
            head_width=0.14,
            body_width=0.02,
        )
        .fill(RULE)
        .no_stroke()
    )
    flow_label = t(
        scene,
        "del diagnóstico del proceso manual a la evaluación con un caso real",
        0,
        -2.35,
        size=0.18,
        color=MUTED,
        anchor=Anchor.TOP,
    )
    scene.play(
        [
            flow.animate.grow_arrow().duration(0.8),
            flow_label.animate.fade_in().duration(0.5),
        ]
    )
    source(scene, "Tesis · cap. 1, Objetivos específicos")
    scene.stop("objetivos-especificos")


def method(scene: Scene) -> None:
    header(
        scene, KICKER, "Investigación aplicada, cuantitativa, sobre un caso de estudio"
    )
    facts = [
        ("Nivel", "Aplicativo"),
        ("Enfoque", "Cuantitativo"),
        ("Diseño", "Caso de estudio"),
        ("Muestra", "No probabilística"),
    ]
    tiles: list[Drawable] = []
    for i, (name, value) in enumerate(facts):
        x0 = LEFT_EDGE + i * 3.72
        tiles.append(scene.geometry.line(x0, 2.4, x0, 1.45).stroke(BRICK, 0.035))
        tiles.append(label(scene, name, x0 + 0.22, 2.38, color=MUTED, size=0.14))
        tiles.append(
            t(
                scene,
                value,
                x0 + 0.22,
                2.08,
                font=DISPLAY,
                size=0.36,
                weight=700,
                color=INK,
            )
        )
    scene.play(stagger(*[x.animate.fade_in().duration(0.35) for x in tiles], each=0.05))
    note = t(
        scene,
        "Un edificio de albañilería confinada de 4 pisos (San Bartolomé, 2006) "
        "para probar el método manual y el marco automatizado.",
        LEFT_EDGE + 0.22,
        1.25,
        size=0.2,
        color=INK_SOFT,
    )
    scene.play(note.animate.fade_in().duration(0.4))

    stages = [
        ("Revisión normativa", "E.030 · E.070 y\nbibliografía"),
        ("Diagramas de flujo", "especificación\nde cada verificación"),
        ("Programa propio", "Python + API\nde ETABS"),
        ("Comparación", "descriptiva entre\nmodelos del caso"),
    ]
    step_items: list[Drawable] = []
    for i, (name, body) in enumerate(stages):
        cx = LEFT_EDGE + 1.6 + i * 3.72
        circle = (
            scene.geometry.circle(0.3)
            .fill(STEEL_SOFT)
            .stroke(STEEL, 0.02)
            .move_to(cx, 0.05)
        )
        num = t(
            scene,
            str(i + 1),
            cx,
            0.05,
            font=DISPLAY,
            size=0.3,
            weight=700,
            color=STEEL,
            anchor=Anchor.CENTER,
        )
        name_t = t(
            scene, name, cx, -0.45, size=0.24, weight=900, color=INK, anchor=Anchor.TOP
        )
        body_t = t(scene, body, cx, -0.82, size=0.19, color=INK_SOFT, anchor=Anchor.TOP)
        step_items.append(scene.geometry.group([circle, num, name_t, body_t]))
        if i:
            step_items.append(
                scene.geometry.line(cx - 3.72 + 0.42, 0.05, cx - 0.42, 0.05).stroke(
                    STEEL, 0.02
                )
            )
    scene.play(
        stagger(
            *[
                s.animate.fade_in_from(Direction.LEFT, 0.1).duration(0.4)
                for s in step_items
            ],
            each=0.12,
        )
    )

    tools = ["ETABS v22", "Python", "Typst", "Excel", "Norma E.030", "Norma E.070"]
    tool_label = label(scene, "Instrumentos", LEFT_EDGE, -2.05, color=MUTED, size=0.14)
    chips: list[Drawable] = []
    x = LEFT_EDGE + 1.75
    for name in tools:
        w_, _ = scene.text.measure(name, size=0.18, font=MONO)
        chips.append(
            pill(
                scene,
                name,
                x,
                -2.1,
                size=0.18,
                color=INK,
                background=PAPER_DEEP,
                anchor=Anchor.LEFT,
            )
        )
        x += w_ + 0.55
    scene.play(
        [
            tool_label.animate.fade_in().duration(0.3),
            stagger(*[c.animate.fade_in().duration(0.25) for c in chips], each=0.06),
        ]
    )
    takeaway(
        scene,
        "Comparación descriptiva: se cuantifican diferencias, no se generaliza a toda la población",
        y=-2.95,
    )
    source(
        scene, "Tesis · cap. 1, Metodología de la investigación; población y muestra"
    )
    scene.stop("metodologia")


SECTION = Section(
    "objetivos",
    [
        SectionStep(
            name="Objetivos · general e hipótesis",
            build=purpose,
            transition=Transition.cross_fade(0.45),
            notes=(
                "45 s. Leer el objetivo general (cap. 1). La cadena ETABS → marco → Alba → "
                "reporte anticipa la estructura de la exposición. Hipótesis: el marco integrado "
                "por API sistematiza extracción, procesamiento, verificación y documentación. "
                "Variables: método (manual o automatizado) y cumplimiento normativo."
            ),
        ),
        SectionStep(
            name="Objetivos · específicos",
            build=specific,
            transition=Transition.cross_fade(0.45),
            notes=(
                "30 s. Cada objetivo específico tiene un producto concreto en la tesis: el flujo "
                "manual (cap. 5), los diagramas de flujo del marco (cap. 6), el programa Alba "
                "conectado por API (cap. 7) y la comparación de modelos del caso (cap. 8). "
                "Los bloques siguientes recorren estos productos en el mismo orden."
            ),
        ),
        SectionStep(
            name="Objetivos · metodología",
            build=method,
            transition=Transition.cross_fade(0.45),
            notes=(
                "45 s. Nivel aplicativo, enfoque cuantitativo, muestra no probabilística: un "
                "caso de estudio (edificio de San Bartolomé, 2006). Técnicas: análisis documental, "
                "modelado FEM, desarrollo de software, verificación del software y comparación "
                "descriptiva. Subrayar que la comparación cuantifica diferencias entre modelos; no "
                "es una validación estadística ni mide ahorro de tiempo."
            ),
        ),
    ],
)
