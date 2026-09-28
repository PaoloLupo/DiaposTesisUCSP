"""Bloque 2 · Objetivos, hipótesis y método de la investigación."""

from gaanim import (
    Anchor,
    Direction,
    Drawable,
    Easing,
    Playable,
    Scene,
    Section,
    SectionStep,
    Transition,
    parallel,
    part,
    sequence,
    stagger,
)

from tesis.kit import LEFT_EDGE, RIGHT_EDGE, header, label, panel, source, t, takeaway
from tesis.theme import (
    BODY,
    BRICK,
    BRICK_DEEP,
    CARD,
    DISPLAY,
    INK,
    INK_SOFT,
    MONO,
    MUTED,
    RULE,
    STEEL,
    STEEL_SOFT,
)

KICKER = "02 · Objetivos y método"


# Cadena del objetivo: cada eslabón y la frase del objetivo general que le corresponde.
CHAIN = (
    ("ETABS", "modelo analizado", "etabs"),
    ("Marco", "procesos y flujos", "marco"),
    ("Alba", "programa propio", "alba"),
    ("Reporte", "memoria trazable", "verificacion"),
)


def purpose(scene: Scene) -> None:
    header(scene, KICKER, "Un marco de trabajo entre ETABS y la verificación E.070")

    tag = label(scene, "Objetivo general", LEFT_EDGE, 2.35, color=BRICK)
    objective = scene.text(
        "Desarrollar ",
        part("marco", "un marco de trabajo"),
        " para la\nautomatización de la ",
        part("verificacion", "verificación normativa"),
        "\nde la distribución de muros en planta de\n"
        "edificios de albañilería confinada (E.070),\naplicado en ",
        part("alba", "un programa propio"),
        " que\ninteractúa con ",
        part("etabs", "el software ETABS"),
        ".",
        style=BODY,
        font=DISPLAY,
        size=0.36,
        weight=400,
        color=INK,
    ).move_to(LEFT_EDGE, 2.0, Anchor.TOP_LEFT)
    scene.play(
        stagger(
            tag.animate.fade_in().duration(0.3),
            objective.animate.reveal(
                style="slide_up", by="line", stagger=0.09
            ).duration(1.0),
            each=0.15,
        )
    )

    # Un paquete de datos recorre la cadena; al llegar a cada eslabón aparece su
    # nombre y se enciende en el objetivo la frase que lo anuncia.
    line_y = -1.55
    xs = [LEFT_EDGE + i * 2.55 for i in range(len(CHAIN))]
    ticks = [
        scene.geometry.line(x, line_y + 0.1, x, line_y - 0.1).stroke(INK_SOFT, 0.02)
        for x in xs
    ]
    segments = [
        scene.geometry.line(a, line_y, b, line_y).stroke(INK_SOFT, 0.016)
        for a, b in zip(xs, xs[1:])
    ]
    packet = (
        scene.geometry.rect(0.14, 0.14)
        .fill(BRICK)
        .no_stroke()
        .move_to(xs[0], line_y)
        .z_index(5)
    )
    hops: list[Playable] = [packet.animate.fade_in().duration(0.15)]
    for i, ((name, sub, key), x) in enumerate(zip(CHAIN, xs, strict=True)):
        proposal = name in ("Marco", "Alba")
        title = t(
            scene,
            name,
            x,
            line_y - 0.22,
            size=0.26,
            weight=900,
            color=BRICK_DEEP if proposal else INK,
        )
        note = t(scene, sub, x, line_y - 0.58, size=0.16, color=INK_SOFT)
        if i:
            hops.append(
                parallel(
                    packet.animate.move_to(x, line_y)
                    .duration(0.5)
                    .easing(Easing.LINEAR),
                    segments[i - 1]
                    .animate.create()
                    .duration(0.5)
                    .easing(Easing.LINEAR),
                )
            )
        hops.append(
            parallel(
                ticks[i].animate.create().duration(0.2),
                title.animate.fade_in_from(Direction.UP, 0.06).duration(0.3),
                note.animate.fade_in().duration(0.3).delay(0.1),
                objective[key].animate.fill(BRICK).duration(0.35),
            )
        )
    hops.append(packet.animate.fade_out().duration(0.2))
    scene.play(sequence(*hops))
    scene.stop("objetivo-general")

    # Hipótesis: el método de verificación (manual → automatizado) incide en el
    # cumplimiento normativo.
    hx, dep_x = 2.5, 5.15
    h_tag = label(scene, "Hipótesis", hx, 2.35, color=STEEL)
    hypothesis = t(
        scene,
        "Un marco automatizado, integrado a ETABS\n"
        "mediante su API, permitirá sistematizar\n"
        "la extracción y el procesamiento de datos\n"
        "del modelo de elementos finitos, así como\n"
        "ejecutar y documentar las verificaciones\n"
        "normativas.",
        hx,
        2.0,
        size=0.23,
        color=INK,
    )
    rule = scene.geometry.line(hx, 0.1, RIGHT_EDGE, 0.1).stroke(RULE, 0.012)
    independent = [
        label(scene, "Variable independiente", hx, -0.15, color=MUTED, size=0.12),
        t(
            scene,
            "Método de\nverificación",
            hx,
            -0.42,
            size=0.22,
            weight=700,
            color=INK,
        ),
    ]
    dependent = [
        label(scene, "Variable dependiente", dep_x, -0.15, color=MUTED, size=0.12),
        t(
            scene,
            "Cumplimiento\nnormativo",
            dep_x,
            -0.42,
            size=0.22,
            weight=700,
            color=INK,
        ),
    ]
    relation = (
        scene.geometry.arrow(
            4.2, -0.68, 4.9, -0.68, head_length=0.14, head_width=0.14, body_width=0.024
        )
        .fill(STEEL)
        .no_stroke()
    )
    levels_y = -1.3
    manual = t(
        scene, "manual", hx, levels_y, size=0.19, color=INK_SOFT, anchor=Anchor.LEFT
    )
    manual_w = manual.bounds().width
    shift = (
        scene.geometry.arrow(
            hx + manual_w + 0.14,
            levels_y,
            hx + manual_w + 0.6,
            levels_y,
            head_length=0.1,
            head_width=0.1,
            body_width=0.016,
        )
        .fill(INK_SOFT)
        .no_stroke()
    )
    automated = t(
        scene,
        "automatizado",
        hx + manual_w + 0.72,
        levels_y,
        size=0.19,
        weight=700,
        color=STEEL,
        anchor=Anchor.LEFT,
    )
    scene.play(
        stagger(
            h_tag.animate.fade_in().duration(0.3),
            hypothesis.animate.reveal(
                style="slide_up", by="line", stagger=0.07
            ).duration(0.8),
            rule.animate.create().duration(0.5),
            each=0.15,
        )
    )
    # Se lee como una relación causal: la variable independiente, sus dos valores
    # y la flecha hacia la dependiente.
    scene.play(
        sequence(
            parallel(
                *[
                    v.animate.fade_in_from(Direction.UP, 0.06).duration(0.35)
                    for v in independent
                ]
            ),
            parallel(
                manual.animate.fade_in().duration(0.25),
                shift.animate.grow_arrow().duration(0.35).delay(0.15),
                automated.animate.fade_in_from(Direction.LEFT, 0.08)
                .duration(0.35)
                .delay(0.4),
            ),
            relation.animate.grow_arrow().duration(0.45),
            parallel(
                *[
                    v.animate.fade_in_from(Direction.UP, 0.06).duration(0.35)
                    for v in dependent
                ]
            ),
        )
    )
    source(
        scene,
        "Tesis · §1.3.1 Objetivo general, §1.4 Hipótesis y §1.5 Variables de la investigación, pp. 3–4",
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
        # El producto de cada objetivo como rótulo técnico, sin etiqueta de color.
        tag = t(
            scene,
            product,
            x0 + 0.3,
            -1.45,
            font=MONO,
            size=0.16,
            color=BRICK_DEEP,
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
    source(scene, "Tesis · §1.3.2 Objetivos específicos, p. 4")
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
        tiles.append(scene.geometry.line(x0, 2.58, x0 + 3.4, 2.58).stroke(RULE, 0.014))
        tiles.append(label(scene, name, x0, 2.38, color=MUTED, size=0.14))
        tiles.append(
            t(
                scene,
                value,
                x0,
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
        LEFT_EDGE,
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
    # Instrumentos en una línea, separados por puntos medios.
    chips: list[Drawable] = []
    x = LEFT_EDGE + 1.75
    for i, name in enumerate(tools):
        chips.append(
            t(scene, name, x, -2.1, font=MONO, size=0.19, color=INK, anchor=Anchor.LEFT)
        )
        x = chips[-1].bounds().right
        if i < len(tools) - 1:
            chips.append(
                t(
                    scene,
                    "·",
                    x + 0.2,
                    -2.1,
                    size=0.19,
                    color=MUTED,
                    anchor=Anchor.CENTER,
                )
            )
            x += 0.4
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
        scene,
        "Tesis · §1.6 Metodología de la investigación y §1.6.3 Población y muestra, p. 5",
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
