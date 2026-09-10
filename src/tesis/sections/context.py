"""
Problemática: contexto nacional → distribución en planta → trabajo manual.
"""

import itertools
from collections.abc import Callable

from gaanim import (
    BLACK,
    ORANGE,
    Anchor,
    Axis,
    ChartSpec,
    Color,
    Direction,
    Drawable,
    Field,
    Scale,
    Scene,
    Section,
    SectionStep,
    Transition,
    computed,
    sequence,
    stagger,
)

from tesis.data.materiales_inei import CHART_DATA, MATERIALES, PORCENTAJES, SOURCE_LABEL
from tesis.theme import (
    ACCENT,
    ARROW_STYLE,
    BODY,
    CENTER_FLOW,
    HEADING,
    INK_MUTED,
    LEFT_FLOW,
    NODE_BODY,
    NODE_CARD,
    NODE_NUMBER,
    NODE_TITLE,
    RULE,
    WARM,
)


def _text(
    scene: Scene,
    content: str,
    x: float,
    y: float,
    *,
    size: float | None = None,
    color: Color | str | None = None,
    center: bool = False,
):
    return (
        scene.text(
            content,
            style=BODY,
            flow=CENTER_FLOW if center else LEFT_FLOW,
            size=size,
            color=color,
        )
        .move_to(x, y, Anchor.CENTER if center else Anchor.TOP_LEFT)
    )


def _header(scene: Scene, headline: str):
    title = scene.text(headline, style=HEADING, flow=CENTER_FLOW).move_to(0, 3.5, Anchor.CENTER)
    rule = scene.geometry.line(length=14).stroke(ACCENT, 0.035).next_to(title, direction=Direction.DOWN, spacing= 0.2 )
    scene.play(
        [
            title.animate.write(),
            rule.animate.create(),
        ],
        duration=0.8,
    )


def materials_inei(scene: Scene):
    _header(scene, "*Albañilería* presente como material\nen un país con alta actividad sísmica")

    # SVG stroke widths are local to the asset and scale with its geometry.
    outline = (
        scene.media.svg("peru.svg")
        .no_fill()
        .stroke(INK_MUTED, 2)
        .scale_to(0.007)
        .move_to(0, -0.2)
    )
    amount = scene.viz.parameter(0.0)
    fraction: Callable[[float], float] = lambda value: value / 100
    percentage = (
        scene.viz.readout(amount, format=".0f", suffix="%", font_size=0.8)
        .fill(BLACK)
        .move_to(0, -1)
    )
    fill = scene.geometry.fill_level(
        outline,
        ACCENT,
        direction="up",
        keep_outline=False,
    ).z_index(-1).set_fill_level(computed(fraction, inputs=[amount]))
    map_group = scene.geometry.group([outline, fill, percentage])
    caption = _text(
        scene,
        "Viviendas con paredes de\n*ladrillo o bloque de concreto*",
        0,
        -3.4,
        size=0.27,
        center=True,
    )
    scene.play([outline.animate.fade_in()])
    scene.play(
        [
            percentage.animate.fade_in(),
            amount.animate.set(PORCENTAJES[0]),
            caption.animate.fade_in(),
        ],
        duration=1.35,
    )
    scene.stop("material-predominante")

    # Explicit overview restoration prevents a map detail from cropping the chart.
    scene.play(
        [
            map_group.animate.shift_by(-4.65, 0),
            caption.animate.shift_by(-4.65, 0),
        ],
        duration=0.85,
    )
    colors = [
        ACCENT,
        "#B7791F",
        "#8B5E3C",
        "#A16207",
        "#64748B",
        "#D97706",
        "#78716C",
        "#94A3B8",
        "#475569",
    ]
    spec = (
        ChartSpec(CHART_DATA, key="id")
        .mark("bar", width=0.72, label_position="outside", label_offset=0.18)
        .encode(
            x="material",
            y="viviendas_porcentaje",
            label="rotulo",
            color=Field(
                "color_material", scale=Scale.category(MATERIALES).colors(colors)
            ),
        )
        .axes(x=Axis.category(MATERIALES), y=Axis.linear(0, 70).ticks(10))
    )
    chart = scene.viz.chart(spec).scale_to(0.68).move_to(2.65, -0.45)
    chart_title = _text(
        scene, "Material predominante en paredes", 2.65, 1.85, size=0.30, center=True
    )
    units = _text(scene, "Viviendas (%)", -1.5, 1.85, size=0.20, color=INK_MUTED)
    source = _text(
        scene,
        f"Fuente: {SOURCE_LABEL}",
        2.65,
        -3.25,
        size=0.19,
        color=INK_MUTED,
        center=True,
    )
    scene.play(
        [
            chart.layer("axes").animate.create(),
            chart_title.animate.fade_in(),
            units.animate.fade_in(),
        ],
        duration=0.65,
    )
    scene.play(
        stagger(
            chart.layer("marks").animate.write().duration(1.0),
            chart.layer("labels").animate.fade_in().duration(0.6),
            source.animate.fade_in().duration(0.4),
            each=0.35,
        )
    )
    scene.stop("materiales-listo")


def _distribution(scene: Scene):
    _header(scene, "La *distribución de muros en planta* es importante")
    # casa = scene.media.svg("edif_alba.svg").scale_by(0.005).move_to(-3.5,0)
    lottie = scene.media.lottie("placas_subduccion.lottie")
    lottie.scale_by(0.8).move_to(-2.5,0)
    scene.play(sequence(lottie.animate.fade_in(), lottie))
    scene.stop("distribucion-y-confinamiento")


def _workflow_node(scene: Scene, x: float, number: str, title: str, body: str):
    labels = [
        (scene.text(number, style=NODE_NUMBER, flow=CENTER_FLOW), 1.2),
        (scene.text(f"*{title}*", style=NODE_TITLE, flow=CENTER_FLOW), 0.3),
        (scene.text(body, style=NODE_BODY, flow=CENTER_FLOW), -0.35),
    ]
    return scene.layout.card([
        scene.layout.item(label, absolute=True, anchor=Anchor.CENTER, offset=(0, y))
        for label, y in labels
    ], **NODE_CARD).move_to(x, 0.65)


def _manual_workflow(scene: Scene):
    _header(scene, "La verificación depende de *pasos manuales*")
    nodes = [
        _workflow_node(
            scene,
            -5,
            "01",
            "Modelo en ETABS",
            "Geometría y resultados\ndel análisis estructural",
        ),
        _workflow_node(
            scene, 0, "02", "Hojas de cálculo", "Extraer, ordenar\ny procesar datos"
        ),
        _workflow_node(
            scene,
            5,
            "03",
            "Verificación E.070",
            "Revisar requisitos\nde la distribución",
        ),
    ]
    arrows = [
        scene.geometry.connector(
            left.port("salida"), right.port("entrada"),
            **ARROW_STYLE,
        )
        .fill(ORANGE).no_stroke()
        for left, right in itertools.pairwise(nodes)
    ]
    transfer = [
        _text(scene, "trasladar", x, 1.13, size=0.18, color=WARM, center=True)
        for x in (-2.5, 2.5)
    ]
    scene.play(
        nodes[0].animate.fade_in_from(Direction.DOWN, distance=0.15), duration=0.55
    )
    for index in range(2):
        scene.play(
            [arrows[index].animate.create(), transfer[index].animate.fade_in()],
            duration=0.45,
        )
        scene.play(
            nodes[index + 1].animate.fade_in_from(Direction.DOWN, distance=0.15),
            duration=0.55,
        )
    scene.stop("flujo-manual")

    risks = [
        _text(scene, text, x, -0.95, size=0.25, color=WARM, center=True)
        for x, text in [
            (-5, "Criterios de modelado"),
            (0, "Transcripción de datos"),
            (5, "Verificaciones omitidas"),
        ]
    ]
    scene.play(
        stagger(*[risk.animate.fade_in().duration(0.45) for risk in risks], each=0.2)
    )
    return_path = (
        scene.geometry.connector(
            nodes[2].port("retorno_inicio"), nodes[0].port("retorno_fin"),
            via=[
                nodes[2].port("retorno_bajada"),
                nodes[0].port("retorno_inferior"),
                nodes[0].port("retorno_giro"),
            ],
            head_length=0.057, head_width=0.15, body_width=0.035,
        )
        .fill(ACCENT).no_stroke()
    )
    repeat = _text(
        scene,
        "Modificar la distribución → repetir la revisión",
        0,
        -2.35,
        size=0.24,
        color=ACCENT,
        center=True,
    )
    scene.play([
        return_path.animate.create().duration(1.15),
        repeat.animate.fade_in().duration(0.8),
    ])
    scene.stop("iteracion-y-riesgos")

    question = _text(
        scene,
        "¿Cómo *sistematizar* la verificación de la distribución de muros?",
        0,
        -3.45,
        size=0.34,
        center=True,
    )
    scene.play(question.animate.write(), duration=1.25)
    scene.stop("pregunta-del-problema")


SECTION = Section("problematica", [
    SectionStep(
        name="Problemática",
        build=materials_inei,
        transition=Transition.cross_fade(0.55),
        notes=(
            "Base: tesis, capítulo 1, Problemática. Introducir la presencia de la "
            "albañilería y el contexto sísmico del Perú. El gráfico actualiza la "
            "referencia INEI 2017 de la tesis con el tabulado de viviendas INEI 2025. "
            "El porcentaje mide material predominante en paredes, no acredita "
            "confinamiento ni desempeño sísmico. El relleno del mapa es un "
            "indicador ilustrativo nacional, no una distribución geográfica."
        ),
    ),
    SectionStep(
        name="Problemática · distribución",
        build=_distribution,
        transition=Transition.cross_fade(0.55),
        notes=(
            "Base: tesis, capítulo 1, Problemática y Justificación. En el "
            "contexto sísmico peruano, explicar la importancia de distribuir "
            "muros portantes en ambas direcciones y conectarlos con los elementos "
            "de confinamiento. La planta es un esquema conceptual sin escala; "
            "no representa el caso de estudio ni demuestra cumplimiento E.070. "
            "No confundir densidad suficiente con una verificación integral."
        ),
    ),
    SectionStep(
        name="Problemática · proceso manual",
        build=_manual_workflow,
        transition=Transition.cross_fade(0.55),
        notes=(
            "Base: tesis, capítulo 1, Problemática (últimos dos párrafos) y "
            "capítulo 5, introducción del análisis manual. Presentar el flujo "
            "convencional estudiado: modelo y resultados en ETABS, extracción "
            "y procesamiento mediante hojas de cálculo, verificaciones E.070. "
            "La tesis identifica variabilidad de criterios, errores de "
            "transcripción y verificaciones omitidas como riesgos, no como "
            "frecuencias medidas. El retorno representa la revisión tras "
            "modificar la distribución. Cerrar con el problema de investigación, "
            "sin anticipar resultados de automatización ni sustituir al ingeniero."
        ),
    ),
])
