"""Bloque 2 · Objetivos, hipótesis y método de la investigación."""

from gaanim import (
    Box,
    Direction,
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

from tesis.components import (
    enter,
    fact,
    hairline,
    header,
    note,
    objective_card,
    page,
    source,
    step,
    takeaway,
)
from tesis.theme import (
    BODY,
    BRICK,
    BRICK_DEEP,
    DISPLAY,
    INK,
    INK_SOFT,
    MONO,
    MUTED,
    STEEL,
)

KICKER = "02 · Objetivos y método"


# Cadena del objetivo: cada eslabón y la frase del objetivo general que le corresponde.
CHAIN = (
    ("ETABS", "modelo analizado", "etabs"),
    ("Marco", "procesos y flujos", "marco"),
    ("Alba", "programa propio", "alba"),
    ("Reporte", "memoria trazable", "norma"),
)


def purpose(scene: Scene) -> None:
    header(scene, KICKER, "Un marco de trabajo entre ETABS y la verificación E.070")
    L = scene.layout

    # Objetivo general: el texto se acomoda al ancho de su columna.
    objective = scene.text(
        "Desarrollar ",
        part("marco", "un marco de trabajo"),
        " para la automatización del diseño de la distribución de muros en planta "
        "para edificios de albañilería confinada conforme a ",
        part("norma", "la norma E.070"),
        ", y su aplicación mediante ",
        part("alba", "un programa de desarrollo propio"),
        " capaz de interactuar con ",
        part("etabs", "el software comercial ETABS"),
        ".",
        style=BODY,
        font=DISPLAY,
        size=0.36,
        weight=400,
        color=INK,
    )
    goal_tag = note(scene, text="Objetivo general", color=BRICK, size="18px")
    goal = L.column(goal_tag, objective, gap="22px", width="fill").item(grow=3)

    # Hipótesis: el método de diseño (manual → automatizado) incide en el
    # cumplimiento normativo. Aparece en la segunda parada.
    relation = scene.geometry.arrow(0, 0, 0.6, 0).fill(STEEL).no_stroke()
    shift = scene.geometry.arrow(0, 0, 0.4, 0).fill(INK_SOFT).no_stroke()
    hyp_tag = note(scene, text="Hipótesis", color=STEEL, size="18px")
    hyp_text = L.box(
        "Un marco automatizado, integrado a ETABS mediante su API, permitirá "
        "sistematizar la extracción y el procesamiento de datos del modelo de "
        "elementos finitos, así como ejecutar y documentar las verificaciones normativas.",
        font_size="27px",
        color=INK,
    )
    independent = L.column(
        note(scene, text="Variable independiente", size="13px"),
        L.box("Método de diseño", font_size="27px", weight=700, color=INK),
        gap="10px",
    ).item(grow=1)
    dependent = L.column(
        note(scene, text="Variable dependiente", size="13px"),
        L.box("Cumplimiento normativo", font_size="27px", weight=700, color=INK),
        gap="10px",
    ).item(grow=1)
    variables = L.row(
        independent,
        L.column(relation, padding=("46px", "0px", "0px", "0px")),
        dependent,
        gap="22px",
        align="start",
        width="fill",
    )
    levels = L.row(
        L.box("manual", font_size="23px", color=INK_SOFT),
        shift,
        L.box("automatizado", font_size="23px", weight=700, color=STEEL),
        gap="16px",
        align="center",
    )
    hypothesis = L.column(
        hyp_tag,
        hyp_text,
        hairline(scene),
        variables,
        levels,
        gap="24px",
        width="fill",
    ).item(grow=2)

    # Cadena del objetivo: un eslabón por columna; un paquete de datos la recorre.
    ticks: list[Box] = []
    segments: list[Box] = []
    titles: list[Box] = []
    subs: list[Box] = []
    cells: list[Box] = []
    for i, (name, sub, _key) in enumerate(CHAIN):
        proposal = name in ("Marco", "Alba")
        tick = L.box(width="2px", height="22px", background=INK_SOFT).item(shrink=0)
        ticks.append(tick)
        line: list[Box] = [tick]
        if i < len(CHAIN) - 1:
            segment = hairline(scene, color=INK_SOFT, thickness="2px")
            segments.append(segment)
            line.append(segment)
        title = L.box(
            name, font_size="31px", weight=900, color=BRICK_DEEP if proposal else INK
        )
        caption = L.box(sub, font_size="19px", color=INK_SOFT)
        titles.append(title)
        subs.append(caption)
        cells.append(
            L.column(
                L.row(*line, align="center", gap="0px", width="fill"),
                title,
                caption,
                gap="10px",
                width="fill",
            ).item(grow=1)
        )
    chain = L.row(*cells, width="1020px", gap="0px")

    top = L.row(goal, hypothesis, gap="56px", align="start", width="fill").item(grow=1)
    page(scene, body=[top, chain], top="190px", bottom="190px", gap="30px")

    scene.play(
        stagger(
            goal_tag.animate.fade_in().duration(0.3),
            objective.animate.reveal(
                style="slide_up", by="line", stagger=0.09
            ).duration(1.0),
            each=0.15,
        )
    )

    # Al llegar a cada eslabón aparece su nombre y se enciende en el objetivo la
    # frase que lo anuncia.
    bounds = [tk.bounds() for tk in ticks]
    xs = [(bd.left + bd.right) / 2 for bd in bounds]
    line_y = (bounds[0].top + bounds[0].bottom) / 2
    packet = (
        scene.geometry.rect(0.14, 0.14)
        .fill(BRICK)
        .no_stroke()
        .move_to(xs[0], line_y)
        .z_index(5)
    )
    hops: list[Playable] = [packet.animate.fade_in().duration(0.15)]
    for i, ((_name, _sub, key), x) in enumerate(zip(CHAIN, xs, strict=True)):
        if i:
            hops.append(
                parallel(
                    packet.animate.move_to(x, line_y)
                    .duration(0.5)
                    .easing(Easing.LINEAR),
                    segments[i - 1]
                    .animate.grow_from_edge(Direction.LEFT)
                    .duration(0.5)
                    .easing(Easing.LINEAR),
                )
            )
        hops.append(
            parallel(
                ticks[i].animate.fade_in().duration(0.2),
                titles[i].animate.fade_in_from(Direction.UP, 0.06).duration(0.3),
                subs[i].animate.fade_in().duration(0.3).delay(0.1),
                objective[key].animate.fill(BRICK).duration(0.35),
            )
        )
    hops.append(packet.animate.fade_out().duration(0.2))
    scene.play(sequence(*hops))
    scene.stop("objetivo-general")

    scene.play(
        enter(
            hypothesis, direction=Direction.UP, distance=0.06, duration=0.4, each=0.12
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
        "un marco de trabajo para\nautomatizar el diseño de la\ndistribución en planta, a partir\nde actividades críticas y\nrepetitivas, con diagramas de flujo.",
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
    cards = [
        objective_card(
            scene,
            number=i + 1,
            verb=verb,
            text=body.replace("\n", " "),
            product=product,
        )
        for i, (verb, body, product) in enumerate(SPECIFIC)
    ]
    flow = scene.layout.column(
        hairline(scene, thickness="3px"),
        note(
            scene,
            text="del diagnóstico del proceso manual a la evaluación con un caso real",
            size="22px",
            upper=False,
        ),
        gap="16px",
        width="fill",
    )
    page(
        scene,
        body=[
            scene.layout.row(*cards, gap="32px", align="stretch", width="fill"),
            flow,
        ],
        gap="48px",
    )
    for card in cards:
        scene.play(
            enter(card, direction=Direction.UP, distance=0.08, duration=0.4, each=0.06)
        )
    scene.play(enter(flow, duration=0.5, each=0.3))
    source(scene, "Tesis · §1.3.2 Objetivos específicos, p. 4")
    scene.stop("objetivos-especificos")


def method(scene: Scene) -> None:
    header(
        scene, KICKER, "Investigación aplicada, cuantitativa, sobre un caso de estudio"
    )
    L = scene.layout
    facts = L.row(
        fact(scene, name="Nivel", value="Aplicativo"),
        fact(scene, name="Enfoque", value="Cuantitativo"),
        fact(scene, name="Diseño", value="Caso de estudio"),
        fact(scene, name="Muestra", value="No probabilística"),
        gap="48px",
        width="fill",
    )
    case = L.box(
        "Un edificio de albañilería confinada de 4 pisos (San Bartolomé, 2006) "
        "para probar el método manual y el marco automatizado.",
        font_size="24px",
        color=INK_SOFT,
    )
    stages = [
        ("Revisión normativa", "E.030 · E.070 y bibliografía"),
        ("Diagramas de flujo", "especificación de cada verificación"),
        ("Programa propio", "Python + API de ETABS"),
        ("Comparación", "descriptiva entre modelos del caso"),
    ]
    steps = L.row(
        *[
            step(scene, number=i + 1, name=name, text=body, last=i == len(stages) - 1)
            for i, (name, body) in enumerate(stages)
        ],
        gap="24px",
        align="start",
        width="fill",
    )
    tools = ["ETABS v22", "Python", "Typst", "Excel", "Norma E.030", "Norma E.070"]
    # Instrumentos en una línea, separados por puntos medios.
    chips: list[Box] = []
    for i, name in enumerate(tools):
        if i:
            chips.append(L.box("·", font_size="23px", color=MUTED))
        chips.append(L.box(name, font=MONO, font_size="23px", color=INK))
    instruments = L.row(
        note(scene, text="Instrumentos"), *chips, gap="24px", align="center"
    )
    conclusion = takeaway(
        scene,
        text="Comparación descriptiva: se cuantifican diferencias, no se generaliza a toda la población",
    )
    page(
        scene,
        body=[facts, case, steps, instruments, conclusion],
        top="215px",
        gap="44px",
    )
    scene.play(enter(facts, direction=Direction.UP, duration=0.35, each=0.05))
    scene.play(case.animate.fade_in().duration(0.4))
    scene.play(enter(steps, distance=0.1, duration=0.4, each=0.12))
    scene.play(enter(instruments, direction=Direction.UP, duration=0.25, each=0.06))
    scene.play(enter(conclusion, direction=Direction.UP, duration=0.5, each=0.1))
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
