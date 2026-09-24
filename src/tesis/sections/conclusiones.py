"""Bloque 8 · Conclusiones: objetivos, hallazgos, alcance y cierre."""

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

from tesis.building import draw_plan
from tesis.data.thesis import (
    DRIFTS,
    SEISMIC_FORCES,
    SEISMIC_WEIGHT,
    crack_failures,
    relative,
)
from tesis.kit import LEFT_EDGE, header, label, panel, source, t
from tesis.theme import (
    BRICK,
    BRICK_DEEP,
    BRICK_SOFT,
    CARD,
    DISPLAY,
    FAIL,
    INK,
    INK_SOFT,
    MUTED,
    PASS,
    PASS_SOFT,
    STEEL,
    STEEL_SOFT,
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
    rows: list[list[Drawable]] = []
    for i, (verb, text) in enumerate(OBJECTIVES):
        y = 2.2 - i * 1.02
        rows.append(
            [
                t(
                    scene,
                    f"{i + 1}",
                    LEFT_EDGE,
                    y + 0.02,
                    font=DISPLAY,
                    size=0.5,
                    weight=700,
                    color=BRICK,
                ),
                t(scene, verb, LEFT_EDGE + 0.6, y, size=0.27, weight=900, color=INK),
                t(scene, text, LEFT_EDGE + 3.0, y, size=0.23, color=INK_SOFT),
                scene.geometry.checkmark(0.26)
                .stroke(PASS, 0.05)
                .no_fill()
                .move_to(6.95, y - 0.25),
                scene.geometry.line(LEFT_EDGE, y - 0.78, 7.3, y - 0.78).stroke(
                    "#E6E0D5", 0.01
                ),
            ]
        )
    for row in rows:
        scene.play(
            stagger(
                *[
                    x.animate.fade_in_from(Direction.LEFT, 0.06).duration(0.35)
                    for x in row
                ],
                each=0.07,
            )
        )
    band = panel(
        scene,
        LEFT_EDGE,
        -2.55,
        14.6,
        1.0,
        fill=PASS_SOFT,
        border=None,
        anchor=Anchor.LEFT,
    )
    tag = label(scene, "Hipótesis", LEFT_EDGE + 0.3, -2.2, color=PASS, size=0.14)
    text = t(
        scene,
        "El marco integrado a ETABS por API sistematiza la extracción, el procesamiento, la "
        "verificación y la documentación.",
        LEFT_EDGE + 0.3,
        -2.45,
        size=0.23,
        weight=700,
        color=INK,
    )
    scene.play(
        [
            band.animate.fade_in().duration(0.3),
            tag.animate.fade_in().duration(0.3),
            text.animate.fade_in_from(Direction.UP, 0.06).duration(0.5),
        ]
    )
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
    w, gap = 3.45, 0.27
    for i, (big, head, body, color) in enumerate(tiles):
        x0 = LEFT_EDGE + i * (w + gap)
        frame = panel(scene, x0, 2.35, w, 3.3, fill=CARD, anchor=Anchor.TOP_LEFT)
        bar = (
            scene.geometry.rect(w - 0.5, 0.05)
            .fill(color)
            .no_stroke()
            .move_to(x0 + w / 2, 2.05)
        )
        value = t(
            scene,
            big,
            x0 + 0.25,
            1.75,
            font=DISPLAY,
            size=0.62,
            weight=700,
            color=color,
        )
        head_t = t(scene, head, x0 + 0.25, 0.8, size=0.23, weight=900, color=INK)
        body_t = t(scene, body, x0 + 0.25, 0.05, size=0.2, color=INK_SOFT)
        scene.play(
            stagger(
                frame.animate.fade_in().duration(0.3),
                bar.animate.create().duration(0.3),
                value.animate.fade_in_from(Direction.UP, 0.08).duration(0.4),
                head_t.animate.fade_in().duration(0.3),
                body_t.animate.fade_in().duration(0.3),
                each=0.08,
            )
        )
    quote = panel(
        scene,
        LEFT_EDGE,
        -1.55,
        14.6,
        1.05,
        fill=BRICK_SOFT,
        border=None,
        anchor=Anchor.TOP_LEFT,
    )
    quote_t = t(
        scene,
        "El criterio del ingeniero sigue siendo el factor determinante: Alba es una herramienta\n"
        "de apoyo, de código libre, para extraer, verificar y documentar.",
        LEFT_EDGE + 0.3,
        -1.7,
        font=DISPLAY,
        size=0.27,
        weight=700,
        color=BRICK_DEEP,
    )
    scene.play(
        [quote.animate.fade_in().duration(0.3), quote_t.animate.fade_in().duration(0.5)]
    )
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
    for x0, title, items, color, soft in [
        (LEFT_EDGE, "Limitaciones", LIMITS, STEEL, STEEL_SOFT),
        (0.25, "Recomendaciones y trabajo futuro", FUTURE, BRICK, BRICK_SOFT),
    ]:
        w = 7.05
        card = panel(scene, x0, 2.35, w, 4.85, fill=CARD, anchor=Anchor.TOP_LEFT)
        band = panel(
            scene,
            x0,
            2.35,
            w,
            0.6,
            fill=soft,
            border=None,
            anchor=Anchor.TOP_LEFT,
            radius=0.1,
        )
        head = t(
            scene,
            title,
            x0 + 0.3,
            2.05,
            size=0.25,
            weight=900,
            color=color,
            anchor=Anchor.LEFT,
        )
        rows: list[Drawable] = []
        for i, item in enumerate(items):
            y = 1.3 - i * 0.78
            rows.append(
                scene.geometry.circle(0.06).fill(color).no_stroke().move_to(x0 + 0.4, y)
            )
            rows.append(
                t(scene, item, x0 + 0.65, y, size=0.23, color=INK, anchor=Anchor.LEFT)
            )
        scene.play(
            stagger(
                card.animate.fade_in().duration(0.3),
                band.animate.fade_in().duration(0.3),
                head.animate.fade_in().duration(0.3),
                stagger(
                    *[
                        r.animate.fade_in_from(Direction.LEFT, 0.06).duration(0.3)
                        for r in rows
                    ],
                    each=0.06,
                ),
                each=0.1,
            )
        )
        scene.stop(f"alcance-{'limites' if color is STEEL else 'futuro'}")
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
    rule = scene.geometry.line(LEFT_EDGE, 0.05, LEFT_EDGE + 1.2, 0.05).stroke(
        BRICK, 0.045
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
            rule.animate.create().duration(0.4),
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
            stagger(
                *[w.animate.grow_from_center().duration(0.35) for w in plan.all_walls],
                each=0.03,
            ),
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
