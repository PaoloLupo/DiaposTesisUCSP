from gaanim import (
    BLACK,
    Anchor,
    Background,
    Direction,
    Scene,
    Theme,
    Transition,
    part,
)

# Identidad visual compartida por la sustentación.
ACCENT = "#1601FC"
INK = "#111827"
MUTED = "#5F6B7A"
PANEL = "#FFFFFF"
PANEL_LINE = "#DCE3F2"
BRICK = "#D97652"
BRICK_DARK = "#A9482A"
CONCRETE = "#334155"
SEISMIC = "#F59E0B"
SAFE = "#16A36A"


SHADER = r"""
fn gaanim_background(uv: vec2<f32>, resolution: vec2<f32>, time: f32) -> vec4<f32> {
    let p = uv - vec2<f32>(0.5);
    let aspect = resolution.x / resolution.y;
    let q = vec2<f32>(p.x * aspect, p.y);

    let paper = vec3<f32>(0.974, 0.978, 0.986);
    let blueprint = vec3<f32>(0.100, 0.065, 0.420);
    let title_blue = vec3<f32>(0.150, 0.105, 0.700);

    let wave_y = q.y
        + 0.040 * sin(q.x * 4.6 - time * 0.10)
        + 0.014 * sin(q.x * 10.0 + time * 0.065);
    let contour_phase = abs(fract((wave_y - 0.28) * 22.0) - 0.5);
    let contours = 1.0 - smoothstep(0.010, 0.032, contour_phase);
    let lower_zone = 1.0 - smoothstep(-0.47, -0.25, q.y);
    let wash = lower_zone * (0.048 + 0.014 * sin(q.x * 2.2 - time * 0.05));
    let contour_ink = contours * lower_zone * 0.046;

    let color = mix(paper, title_blue, wash);
    let final_color = mix(color, blueprint, contour_ink);
    return vec4<f32>(final_color, 1.0);
}
"""


scene = Scene(
    1920,
    1080,
    background=Background.shader(SHADER, fallback="#F6F8FC"),
    margin=64,
    theme=Theme("paper"),
)
scene.load_project()


# ---------------------------------------------------------------------------
# 1. PORTADA
# ---------------------------------------------------------------------------
scene.segment(
    "Título",
    notes=(
        "Presentar el tema, a los tesistas y al asesor. "
        "Enfatizar que el aporte central es un marco de trabajo automatizado."
    ),
)

title_accent = scene.line(-850, -150, 850, -150).stroke(ACCENT, 7)
logo = scene.svg("logoucsp.svg").scaled(0.15).at(0, 400).fill(BLACK)
escuela = scene.text(
    "*UNIVERSIDAD CATÓLICA SAN PABLO*\n"
    "Facultad de Arquitectura, Computación e Ingenierías\n"
    "Escuela Profesional de Ingeniería Civil",
    text_align="center",
    line_spacing=1.4,
).at(0, 250)
title = scene.text(
    "*MARCO DE TRABAJO PARA LA AUTOMATIZACIÓN DEL DISEÑO DE LA DISTRIBUCIÓN "
    "DE MUROS EN PLANTA PARA EDIFICIOS DE ALBAÑILERÍA CONFINADA*",
    role="title",
    text_align="center",
    line_spacing=1.35,
).at(0, 0)
authors = scene.text(
    "Paolo Cesar Guillen Lupo  •  Pamela Lucyla Banda Alarta\n"
    "*Asesor:* Mgtr. David Miguel Chalco Pari",
    text_align="center",
    line_spacing=1.8,
).at(0, -260)

scene.play(
    [
        logo.fade_in().duration(0.5),
        escuela.fade_in_from(Direction.DOWN, distance=24).duration(0.7),
    ]
)
scene.play(
    [
        title.write(1.0, by="word"),
        title_accent.create().duration(0.8),
    ]
)
scene.play([authors.fade_in_from(Direction.DOWN, distance=24).duration(0.6)])
scene.stop("portada-lista")


# ---------------------------------------------------------------------------
# 2. CONTEXTO DEL PROBLEMA
# ---------------------------------------------------------------------------
scene.segment(
    "Contexto del problema",
    Transition.cross_fade(0.55),
    notes=(
        "La albañilería es el material predominante en más de la mitad de las "
        "viviendas urbanas del Perú. Su uso económico y extendido convive con "
        "una alta amenaza sísmica. Por ello el diseño debe articular la demanda "
        "de la E.030 con los requisitos específicos de albañilería de la E.070."
    ),
)

# Encabezado editorial.
eyebrow = scene.text("02  /  CONTEXTO DEL PROBLEMA").fill(ACCENT).scaled(0.72).at(
    -850, 455, Anchor.TOP_LEFT
)
headline = scene.text(
    "Un sistema constructivo *masivo*\n"
    "en un país de *alta actividad sísmica*",
    role="title",
    line_spacing=1.15,
).fill(INK).scaled(0.90).at(-850, 385, Anchor.TOP_LEFT)
header_rule = scene.line(-850, 245, 850, 245).stroke(PANEL_LINE, 3)

scene.play(
    [
        eyebrow.fade_in_from(Direction.DOWN, distance=18).duration(0.45),
        headline.write(0.95, by="word"),
        header_rule.create().duration(0.65),
    ]
)

# Dato principal: se mantiene deliberadamente grande y breve.
stat = scene.text(
    part("value", "> 1/2", color=ACCENT),
    "\nde las viviendas urbanas",
    text_align="center",
    line_spacing=1.10,
).at(-560, 125)
stat_caption = scene.text(
    "usa albañilería como\nmaterial predominante",
    text_align="center",
    line_spacing=1.20,
).fill(MUTED).scaled(0.76).at(-560, 18)

scene.play(
    [
        stat.grow_from_center().duration(0.65).spring(),
        stat_caption.fade_in_from(Direction.DOWN, distance=22).duration(0.55),
    ]
)
scene.play([stat["value"].indicate(duration=0.55)])


# Edificio esquemático de albañilería confinada: muros, columnas y vigas.
building_parts = []
wall_panels = []
for floor in range(3):
    y = -115 - floor * 105
    for bay in range(2):
        x = -680 + bay * 240
        panel = (
            scene.rounded_rect(205, 78, 7)
            .fill(BRICK)
            .stroke(BRICK_DARK, 2)
            .at(x, y)
        )
        wall_panels.append(panel)
        building_parts.append(panel)

columns = [
    scene.rect(28, 330).fill(CONCRETE).at(-800, -220),
    scene.rect(28, 330).fill(CONCRETE).at(-560, -220),
    scene.rect(28, 330).fill(CONCRETE).at(-320, -220),
]
beams = [
    scene.rect(508, 24).fill(CONCRETE).at(-560, -61 - floor * 105)
    for floor in range(4)
]
foundation = scene.rounded_rect(580, 34, 8).fill(CONCRETE).at(-560, -404)
building_parts.extend(columns)
building_parts.extend(beams)
building_parts.append(foundation)
building = scene.group(building_parts)

scene.play([foundation.grow_from_center().duration(0.38)])
scene.play([panel.draw_border_then_fill().duration(0.65) for panel in wall_panels])
scene.play(
    [column.grow_from_center().duration(0.55) for column in columns]
    + [beam.grow_from_center().duration(0.55) for beam in beams]
)


# La acción sísmica introduce la necesidad normativa.
seismic_wave = scene.path(
    [
        (-875, -455),
        (-820, -455),
        (-790, -425),
        (-755, -485),
        (-715, -440),
        (-675, -468),
        (-625, -455),
        (-250, -455),
    ]
).no_fill().stroke(SEISMIC, 8)
seismic_label = scene.badge(
    "ALTA ACTIVIDAD SÍSMICA",
    color=SEISMIC,
    background="#FFF7E6",
    padding=(28, 14),
    radius=13,
).scaled(0.76)

scene.play(
    [
        seismic_wave.create().duration(0.85),
        seismic_label.grow_from_center().duration(0.55),
        building.wiggle().duration(0.85),
    ]
)


# Dos filtros normativos complementarios.
card_030_bg = (
    scene.rounded_rect(650, 150, 24)
    .fill(PANEL)
    .stroke("#B9C5FF", 3)
    .at(480, 105)
)
card_030_code = scene.text("*E.030*").fill(ACCENT).scaled(1.28).at(270, 115)
card_030_text = scene.text(
    "*Diseño sismorresistente*\n"
    "Define la demanda y controla las distorsiones",
    line_spacing=1.25,
).fill(INK).scaled(0.64).at(390, 150, Anchor.TOP_LEFT)
card_030 = scene.group([card_030_bg, card_030_code, card_030_text])

card_070_bg = (
    scene.rounded_rect(650, 150, 24)
    .fill(PANEL)
    .stroke("#A8E1C8", 3)
    .at(480, -105)
)
card_070_code = scene.text("*E.070*").fill(SAFE).scaled(1.28).at(270, -95)
card_070_text = scene.text(
    "*Albañilería*\n"
    "Exige densidad, resistencia y confinamiento",
    line_spacing=1.25,
).fill(INK).scaled(0.64).at(390, -60, Anchor.TOP_LEFT)
card_070 = scene.group([card_070_bg, card_070_code, card_070_text])

arrow_030 = scene.arrow(-210, -105, 100, 85).fill(ACCENT)
arrow_070 = scene.arrow(-210, -150, 100, -95).fill(SAFE)

scene.play(
    [
        arrow_030.create().duration(0.55),
        card_030.fade_in_from(Direction.RIGHT, distance=54).duration(0.65),
    ]
)
scene.play(
    [
        arrow_070.create().duration(0.55),
        card_070.fade_in_from(Direction.RIGHT, distance=54).duration(0.65),
    ]
)

# Síntesis que prepara la diapositiva 3 (el proceso tradicional).
takeaway_bg = (
    scene.rounded_rect(720, 100, 22)
    .fill("#EEF1FF")
    .stroke("#C6CEFF", 2)
    .at(445, -315)
)
takeaway_icon = scene.checkmark(25).fill(ACCENT).at(135, -315)
takeaway = scene.text(
    "El diseño debe *conectar* el modelo estructural\n"
    "con ambas verificaciones normativas.",
    line_spacing=1.22,
).fill(INK).scaled(0.78).at(485, -315)
takeaway_group = scene.group([takeaway_bg, takeaway_icon, takeaway])

source = scene.text(
    "Fuente: tesis, cap. 1 (INEI 2017; NTE E.030 y NTE E.070)",
).fill(MUTED).scaled(0.52).at(850, -486, Anchor.BOTTOM_RIGHT)

scene.play(
    [
        takeaway_group.fade_in_from(Direction.DOWN, distance=30).duration(0.65),
        source.fade_in().duration(0.45),
    ]
)
scene.play([takeaway.indicate().duration(0.55)])
scene.stop("contexto-listo")


scene.render()
