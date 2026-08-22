from pathlib import Path

from gaanim import (
    BLACK,
    BLUE,
    GRAY,
    ORANGE,
    PURPLE,
    RED,
    WHITE,
    Anchor,
    Background,
    Brush,
    Direction,
    Scene,
    Transition,
)

# ---------------------------------
# COLORES
# ---------------------------------

ACCENT = "#1601FC"

scene = Scene(
    1920,
    1080,
    background=Background.shader(Path("assets/background.wgsl"), fallback="#03060B"),
    margin=80,
)
scene.load_project()
scene.canvas.set_theme("paper")

# ---------------------------------
# TITULO
# ---------------------------------
_ = scene.segment("Titulo")
logo = scene.svg("logoucsp.svg").scaled(0.15).at(0, 400).fill(BLACK)
faculty = scene.text(
    "*UNIVERSIDAD CATÓLICA SAN PABLO*\nFacultad de Arquitectura, Computación e Ingenierías\nEscuela Profesional de Ingeniería Civil",
    text_align="center",
    line_spacing=1.4,
).at(0, 250)
title = scene.text(
    "*MARCO DE TRABAJO PARA LA AUTOMATIZACIÓN DEL DISEÑO DE LA DISTRIBUCIÓN DE MUROS EN PLANTA PARA EDIFICIOS DE ALBAÑILERÍA CONFINADA*",
    role="title",
    text_align="center",
    line_spacing=1.35,
).at(0, 0)
title_accent = scene.line(-880, -150, 880, -150).stroke(ACCENT, 7)
authors = scene.text(
    "Paolo Cesar Guillen Lupo  •  Pamela Lucyla Banda Alarta\n*Asesor:* Mgtr. David Miguel Chalco Pari",
    text_align="center",
    line_spacing=1.8,
).at(0, -260)

scene.play(
    [
        logo.fade_in(),
        faculty.fade_in(),
        title.write(),
        title_accent.create(),
        authors.fade_in(),
    ]
)

scene.stop()

# ---------------------------------
# CONTEXTO DEL PROBLEMA
# ---------------------------------

_ = scene.segment("Contexto del problema", Transition.cross_fade(0.55))

eyebrow = (
    scene.text("02  /  CONTEXTO DEL PROBLEMA")
    .fill(ACCENT)
    .scaled(0.72)
    .at(-880, 450, Anchor.TOP_LEFT)
)

headline = (
    scene.text(
        "La *albañilería confinada* como sistema constructivo *masivo*\nen un país con *alta actividad sísmica*",
        role="title",
    )
    .fill(BLACK)
    .at(-880, 400, Anchor.TOP_LEFT)
)
title_accent = scene.line(-880, 270, 880, 270).stroke(ACCENT, 5)
# inei_text = scene.text("Según INEI,").at(0,0)

# edif_svg = scene.svg("edif_alba.svg").scaled(0.5).at(-550, -100)
mapa_peru_mask = (
    scene.svg("peru.svg").no_fill().stroke(BLACK, 3).scaled(0.8).at(0, -100)
)

porcentaje_alb = scene.parameter(0.0)
porcentaje_alb_txt = scene.readout(porcentaje_alb, format=".0f", suffix = "%", font_size=110).at(0,-200).glow(BLACK,3).fill(BLACK)
# TODO: eliminar el artificio de opacity(0) cuando se arregle el bug #3
mapa_peru = scene.fill_level(
    mapa_peru_mask,
    ORANGE,
    0.0,
    direction="up",
    keep_outline=False,
).opacity(0).z_index(-1)
# porcentaje = scene.badge(
#     "$+50 %$ viviendas construidas\nen zonas urbanas",
#     variant="accent",
#     appearance="soft",
# ).at(-100, -100)


scene.play(
    [
        eyebrow.fade_in_from(direction=Direction.DOWN, distance=20),
        headline.write(),
        title_accent.create(),
        mapa_peru_mask.write(),
    ]
)

scene.stop()

scene.play(
    [
        # edif_svg.write(1.5),
        mapa_peru_mask.animate().stroke(GRAY,2),

        scene.camera.frame_to(mapa_peru_mask, margin=0, duration=1.2),
        porcentaje_alb_txt.fade_in(),
        porcentaje_alb.animate_to(55.0),
        # TODO: eliminar el artificio de opacity(0) cuando se arregle el bug #3
        mapa_peru.animate().opacity(1).fill_level(0.55).duration(1.2),
    ]
)

scene.stop()

scene.render()
