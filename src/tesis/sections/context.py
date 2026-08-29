from gaanim import (
    BLACK,
    GRAY,
    ORANGE,
    Anchor,
    Axis,
    ChartSpec,
    Direction,
    Field,
    Scale,
    Scene,
    Transition,
    stagger,
)

from tesis.data.materiales_inei import CHART_DATA, MATERIALES
from tesis.theme import ACCENT


def build(scene: Scene):
    _ = scene.segment("Contexto del problema", Transition.cross_fade(0.55))

    eyebrow = (
        scene.text("02  /  CONTEXTO DEL PROBLEMA")
        .fill(ACCENT)
        .scale_to(0.72)
        .move_to(-7.3333, 3.75, Anchor.TOP_LEFT)
    )

    headline = (
        scene.text(
            "La *albañilería confinada* como sistema constructivo *masivo*\nen un país con *alta actividad sísmica*",
            role="title",
        )
        .fill(BLACK)
        .move_to(-7.3333, 3.3333, Anchor.TOP_LEFT)
    )
    title_accent = scene.geometry.line(-7.3333, 2.3333, 7.3333, 2.3333).stroke(
        ACCENT, 0.0417
    )

    # edif_svg = scene.media.svg("edif_alba.svg").scale_to(0.5).move_to(-4.5833, -0.8333)
    mapa_peru_mask = (
        scene.media.svg("peru.svg")
        .no_fill()
        .stroke(BLACK, 0.006)
        .scale_to(0.0066667)
        .move_to(0, -0.8333)
    )

    porcentaje_alb = scene.viz.parameter(0.0)
    porcentaje_alb_txt = (
        scene.viz.readout(porcentaje_alb, format=".0f", suffix="%", font_size=0.9167)
        .move_to(-0.125, -1.6667)
        .glow(BLACK, 0.025)
        .fill(BLACK)
    )
    mapa_peru = scene.geometry.fill_level(
        mapa_peru_mask,
        ORANGE,
        0.0,
        direction="up",
        keep_outline=False,
    ).z_index(-1)

    peru_group = scene.geometry.group([mapa_peru_mask, porcentaje_alb_txt, mapa_peru])

    colores_materiales = [
        ORANGE,
        "#B7791F",
        "#8B5E3C",
        "#A16207",
        "#64748B",
        "#D97706",
        "#78716C",
        "#94A3B8",
        "#475569",
    ]

    materiales_spec = (
        ChartSpec(CHART_DATA, key="id")
        .mark("bar", width=0.72, label_position="outside", label_offset=0.2)
        .encode(
            x="material",
            y="viviendas_porcentaje",
            color=Field(
                "color_material",
                scale=Scale.category(MATERIALES).colors(colores_materiales),
            ),
            label="rotulo",
        )
        .axes(
        x=Axis.category(MATERIALES).label("Material predominante"),
            y=Axis.linear(0, 70).ticks(10).label("Viviendas (%)"),
        )
    )
    materiales_title = (
        scene.text(
            "Material de construcción predominante en paredes",
            role="subtitle",
        )
        .fill(BLACK)
        .scale_to(0.50)
        .move_to(2.0833, 1.0833)
    )

    materiales_chart = (
        scene.viz.chart(materiales_spec).scale_to(0.50).move_to(2.0833, -0.5833)
    )
    materiales_fuente = (
        scene.text("_Fuente: INEI 2025_", role="caption")
        .scale_to(0.5)
        .move_to(4.4167, -2.5833)
        .fill(GRAY)
    )
    materiales_group = scene.geometry.group(
        [materiales_chart.drawable(), materiales_fuente, materiales_title]
    )

    autoconstruccion_txt = scene.slides.badge(
        "En su mayoría autoconstruidas", variant="danger"
    ).move_to(2.0833, -2.5)
    # edif_svg = scene.media.svg("edif_alba.svg").scale_to(0.5).move_to(-4.5833, -0.8333)

    scene.play(
        [
            eyebrow.animate.fade_in_from(direction=Direction.DOWN, distance=0.1667),
            headline.animate.write(),
            title_accent.animate.create(),
            mapa_peru_mask.animate.write(),
        ]
    )

    scene.stop()

    scene.play(
        [
            # edif_svg.write(1.5),
            scene.camera.animate.frame_to(mapa_peru_mask, margin=0).duration(1.2),
            mapa_peru_mask.animate.stroke(GRAY, 0.006),
            porcentaje_alb_txt.animate.fade_in(),
            porcentaje_alb.animate.set(61.8),
            mapa_peru.animate.fill_level(0.55).duration(1.2),
        ]
    )
    scene.wait(1)

    scene.play(
        [
            peru_group.animate.shift_by(-3.3333, 0).duration(1.0),
        ]
    )

    scene.play(
        [
            materiales_chart.layer("axes").animate.create(),
            materiales_title.animate.fade_in_from(
                Direction.DOWN, distance=0.1667
            ).duration(0.5),
        ]
    )
    scene.play(
        stagger(
            materiales_chart.layer("marks").animate.write().duration(1.1),
            materiales_chart.layer("labels").animate.write().duration(1.5),
            materiales_fuente.animate.write(),
            each=1,
        ),
    )

    scene.stop("materiales-listo")

    scene.play(
        [
            materiales_group.animate.shift_by(0, 0.8333),
            autoconstruccion_txt.animate.fade_in(),
        ]
    )

    scene.stop()
