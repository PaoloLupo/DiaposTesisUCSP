"""Bloque 8 · Conclusiones: objetivos, hallazgos, alcance y cierre."""

from gaanim import (
    Direction,
    Scene,
    Section,
    SectionStep,
    Transition,
    stagger,
)

from tesis.building import draw_plan, grow_walls
from tesis.components import (
    column_list,
    enter,
    header,
    numbered_row,
    page,
    source,
    stat_card,
    takeaway,
)
from tesis.data.thesis import (
    DRIFTS,
    SEISMIC_FORCES,
    SEISMIC_WEIGHT,
    crack_failures,
    relative,
)
from tesis.kit import LEFT_EDGE, t
from tesis.theme import (
    BRICK,
    DISPLAY,
    FAIL,
    INK,
    INK_SOFT,
    MUTED,
    STEEL,
)

KICKER = "08 · Conclusiones"

OBJECTIVES = [
    (
        "Identificar",
        "La extracción de resultados, la clasificación de muros y la transcripción\n"
        "a plantillas son actividades críticas y automatizables.",
    ),
    (
        "Desarrollar",
        "Se especificaron procesos, diagramas de flujo y trazabilidad para densidad,\n"
        "esfuerzo axial, fisuración, resistencia al corte y derivas.",
    ),
    (
        "Aplicar",
        "Alba se conecta con ETABS mediante su API, ejecuta las verificaciones y\n"
        "entrega diagnósticos visuales y reportes técnicos automáticos.",
    ),
    (
        "Evaluar",
        "En el caso, el modelo completo permitió extraer y organizar fuerzas, masas y\n"
        "deformaciones; la idealización cambia resultados y diagnósticos.",
    ),
]


def objectives(scene: Scene) -> None:
    header(scene, KICKER, "Los cuatro objetivos se cumplieron en el caso de estudio")
    rows = [
        numbered_row(scene, number=i + 1, name=verb, text=text.replace("\n", " "))
        for i, (verb, text) in enumerate(OBJECTIVES)
    ]
    hypothesis = takeaway(
        scene,
        tag="Hipótesis",
        text="El marco integrado a ETABS por API sistematiza la extracción, el "
        "procesamiento, la verificación y la documentación.",
        display=False,
    )
    page(scene, body=[*rows, hypothesis], top="220px", gap="24px")
    for row in rows:
        scene.play(enter(row))
    scene.play(enter(hypothesis, direction=Direction.UP, each=0.15))
    source(
        scene,
        "Tesis · Conclusiones, p. 135 · se sostiene para el caso estudiado (muestra no probabilística)",
    )
    scene.stop("objetivos-cumplidos")


def findings(scene: Scene) -> None:
    header(scene, KICKER, "Lo que muestra el caso: idealización, norma y criterio")
    weight_gap = relative(SEISMIC_WEIGHT[0], SEISMIC_WEIGHT[1])
    force_gap = max(
        relative(SEISMIC_FORCES["MCT"][i], SEISMIC_FORCES["MSTA"][i]) for i in range(4)
    )
    drift_gap = relative(DRIFTS["X"]["MCT"][3], DRIFTS["X"]["MSTA"][3])
    norm_gap = relative(DRIFTS["X"]["MSTA"][2], DRIFTS["X"]["MSTO"][2])
    cracks = len(crack_failures("MSTA"))
    tiles = [
        (
            f"{weight_gap:.2f} %",
            "peso sísmico MSTA vs MCT",
            f"y fuerzas por nivel con\nvariación ≤ {force_gap:.2f} %",
            BRICK,
        ),
        (
            f"{drift_gap:.2f} %",
            "menos deriva con MCT",
            "el modelo de áreas evita\nconservadurismo innecesario",
            BRICK,
        ),
        (
            f"{norm_gap:.2f} %",
            "menos deriva por columnas\nde 0.25 m (propuesta E.070)",
            "compensa la mayor exigencia\nde la E.030 vigente",
            STEEL,
        ),
        (
            f"{cracks} de 24",
            "muros de MSTA fallan\nfisuración en el piso 1",
            "con MCT, ninguno: el\ndiagnóstico depende del modelo",
            FAIL,
        ),
    ]
    cards = [
        stat_card(scene, value=big, title=head, detail=body, color=color)
        for big, head, body, color in tiles
    ]
    quote = takeaway(
        scene,
        text="El criterio del ingeniero sigue siendo el factor determinante: Alba es una "
        "herramienta de apoyo, de código libre, para extraer, verificar y documentar.",
    )
    page(
        scene,
        body=[
            scene.layout.row(*cards, gap="32px", align="stretch", width="fill"),
            quote,
        ],
        gap="56px",
    )
    for card in cards:
        scene.play(
            enter(card, direction=Direction.UP, distance=0.08, duration=0.3, each=0.08)
        )
    scene.play(enter(quote, direction=Direction.UP, duration=0.5, each=0.1))
    source(
        scene,
        "Tesis · Tablas 50, 51 y 52, pp. 129–131; Tabla 36, p. 87; Conclusiones, p. 135",
    )
    scene.stop("hallazgos")


LIMITS = [
    "Requiere un modelo de ETABS ya elaborado y analizado",
    "Depende de etiquetas Pier únicas y bien asignadas",
    "No modifica el modelo: el ingeniero decide los cambios",
    "Un confinamiento en T o L no puede pertenecer a dos Pier",
    "Un solo caso de estudio: resultados no generalizables",
]
FUTURE = [
    "Diseño automático de los elementos de confinamiento",
    "Asignación de fuerzas en intersecciones T y L",
    "Análisis no lineal con macromodelos de albañilería",
    "Redes neuronales para detectar irregularidades en planta",
    "Mantener Alba al día con el RNE y usarlo en docencia",
]


def outlook(scene: Scene) -> None:
    header(scene, KICKER, "Alcance actual y líneas de continuidad")
    limits = column_list(scene, title="Limitaciones", items=LIMITS, color=STEEL)
    future = column_list(
        scene, title="Recomendaciones y trabajo futuro", items=FUTURE, color=BRICK
    )
    page(
        scene,
        body=[
            scene.layout.row(limits, future, gap="60px", align="start", width="fill")
        ],
        top="230px",
    )
    scene.play(enter(limits, each=0.06, duration=0.3))
    scene.stop("alcance-limites")
    scene.play(enter(future, each=0.06, duration=0.3))
    scene.stop("alcance-futuro")
    source(
        scene,
        "Tesis · Tabla 49, p. 125; §8.2.4, p. 132; Recomendaciones, p. 137",
    )
    scene.stop("alcance-fuente")


def closing(scene: Scene) -> None:
    plan = draw_plan(scene, (3.9, 0.0), 6.3, drawn_thickness=0.075)
    thanks = t(
        scene, "Gracias", LEFT_EDGE, 1.7, font=DISPLAY, size=1.2, weight=700, color=INK
    )
    prompt = t(
        scene,
        "Quedamos atentos a las preguntas\ny observaciones del jurado.",
        LEFT_EDGE,
        -0.25,
        size=0.3,
        color=INK_SOFT,
    )
    authors = t(
        scene,
        "Paolo Cesar Guillen Lupo  ·  Pamela Lucyla Banda Alarta",
        LEFT_EDGE,
        -1.65,
        size=0.22,
        weight=700,
        color=INK,
    )
    advisor = t(
        scene,
        "Asesor: Mgtr. David Miguel Chalco Pari",
        LEFT_EDGE,
        -2.05,
        size=0.2,
        color=MUTED,
    )
    scene.play(
        stagger(
            thanks.animate.fade_in_from(Direction.UP, 0.12).duration(0.7),
            prompt.animate.fade_in().duration(0.5),
            authors.animate.fade_in().duration(0.4),
            advisor.animate.fade_in().duration(0.4),
            each=0.15,
        )
    )
    scene.play(
        stagger(
            stagger(*[g.animate.create().duration(0.5) for g in plan.grid], each=0.03),
            stagger(
                *[b.animate.fade_in().duration(0.25) for b in plan.bubbles], each=0.02
            ),
            plan.slab.animate.fade_in().duration(0.5),
            plan.void.animate.fade_in().duration(0.3),
            grow_walls(plan.all_walls, total=0.9, duration=0.35),
            each=0.2,
        )
    )
    scene.stop("preguntas")


SECTION = Section(
    "conclusiones",
    [
        SectionStep(
            name="Conclusiones · objetivos",
            build=objectives,
            transition=Transition.cross_fade(0.45),
            notes=(
                "1 min. Retomar cada objetivo específico con su conclusión (Conclusiones, p. 135). La hipótesis se "
                "sostiene para el caso: el marco integra de forma reproducible extracción, "
                "procesamiento, verificación y documentación. No se afirma una reducción medida de "
                "tiempo o de errores: no se midió."
            ),
        ),
        SectionStep(
            name="Conclusiones · hallazgos",
            build=findings,
            transition=Transition.cross_fade(0.45),
            notes=(
                "1 min. Cifras de respaldo: peso 1.04 % y Fi ≤ 2.14 % entre MCT y MSTA; derivas de MCT "
                "hasta 13.65 % menores; las columnas de 0.25 m (propuesta E.070) reducen derivas hasta "
                "22.61 % frente a MSTO; 7 de 24 muros de MSTA no cumplen fisuración en el piso 1 y "
                "ninguno en MCT. Cerrar con el rol del criterio del ingeniero."
            ),
        ),
        SectionStep(
            name="Conclusiones · alcance y futuro",
            build=outlook,
            transition=Transition.cross_fade(0.45),
            notes=(
                "45 s. Limitaciones de la implementación (Tabla 49, p. 125) y del estudio (un "
                "caso). Recomendaciones (p. 137): diseño de confinamientos, intersecciones T/L, "
                "análisis no lineal, CNN para irregularidades, mantenimiento del código libre y uso "
                "educativo."
            ),
        ),
        SectionStep(
            name="Cierre",
            build=closing,
            transition=Transition.cross_fade(0.6),
            notes="Agradecer y abrir la ronda de preguntas. Mantener esta diapositiva durante la discusión.",
        ),
    ],
)
