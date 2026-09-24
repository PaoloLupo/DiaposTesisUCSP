"""Bloque 1 · Problemática: material, sistema sísmico y traslado manual de datos."""

from gaanim import (
    Anchor,
    Direction,
    Drawable,
    Scene,
    Section,
    SectionStep,
    Transition,
    computed,
    sequence,
    stagger,
)

from tesis.data.materiales_inei import (
    MATERIALES_ORDENADOS,
    SOURCE_LABEL,
    TOTAL_VIVIENDAS,
)
from tesis.data.thesis import CRACKING_FLOOR1
from tesis.kit import header, label, panel, pill, source, t, takeaway
from tesis.theme import (
    BRICK,
    BRICK_DEEP,
    BRICK_SOFT,
    CARD,
    CONCRETE,
    CONCRETE_SOFT,
    DISPLAY,
    FAINT,
    INK,
    INK_SOFT,
    MONO,
    MUTED,
    PAPER_DEEP,
    RULE,
    STEEL,
    STEEL_SOFT,
)

KICKER = "01 · Problemática"
MATERIAL_LABELS = {
    "Ladrillo\no bloque": "Ladrillo o bloque de concreto",
    "Adobe": "Adobe",
    "Madera": "Madera",
    "Tapia": "Tapia",
    "Triplay\ncalamina\nestera": "Triplay, calamina o estera",
    "Quincha": "Quincha",
    "Piedra\nbarro": "Piedra con barro",
    "Piedra\nsillar": "Piedra o sillar",
    "Otro": "Otro material",
}


def materials(scene: Scene) -> None:
    header(scene, KICKER, "El ladrillo es el material de seis de cada diez viviendas")

    outline = (
        scene.media.svg("peru.svg")
        .no_fill()
        .stroke(INK_SOFT, 1.6)
        .scale_to(0.0058)
        .move_to(-4.75, -0.15)
    )
    counter = scene.viz.rolling_number(
        0,
        decimals=1,
        suffix=" %",
        font_family=DISPLAY,
        weight=700,
        font_size=0.72,
        mode="continuous",
        color=INK,
    ).move_to(-4.55, -0.35, Anchor.CENTER)
    level = computed(lambda value: value / 100, inputs=[counter.parameter])
    fill = (
        scene.geometry.fill_level(
            outline, BRICK_SOFT, direction="up", keep_outline=False
        )
        .z_index(-1)
        .set_fill_level(level)
    )
    caption = t(
        scene,
        "de las viviendas del Perú tienen paredes\nde ladrillo o bloque de concreto",
        -4.75,
        -2.5,
        size=0.2,
        color=INK_SOFT,
        anchor=Anchor.TOP,
    )

    scene.play(outline.animate.create().duration(1.0))
    scene.play(
        [
            counter.visual.animate.fade_in().duration(0.3),
            caption.animate.fade_in().duration(0.5),
        ]
    )
    scene.play(
        counter.count_to(
            100 * MATERIALES_ORDENADOS[0][1] / TOTAL_VIVIENDAS, duration=1.6, snap=True
        )
    )
    scene.stop("material-predominante")

    # Barras horizontales: una sola serie destacada y el resto en gris cálido.
    label_x, bar_x, bar_max = 1.35, 1.55, 4.6
    top, gap = 2.2, 0.56
    scale = bar_max / 70
    title = label(
        scene,
        "Material predominante en paredes exteriores · % de viviendas",
        -1.6,
        2.62,
        color=MUTED,
        size=0.14,
    )
    rows: list[Drawable] = []
    bars: list[Drawable] = []
    for i, (name, count) in enumerate(MATERIALES_ORDENADOS):
        share = 100 * count / TOTAL_VIVIENDAS
        y = top - i * gap
        lead = i == 0
        rows.append(
            t(
                scene,
                MATERIAL_LABELS[name],
                label_x,
                y,
                size=0.22,
                weight=900 if lead else 400,
                color=INK if lead else INK_SOFT,
                anchor=Anchor.RIGHT,
            )
        )
        mask = (
            scene.geometry.rounded_rect(max(share * scale, 0.04), 0.3, 0.04)
            .no_fill()
            .no_stroke()
            .move_to(bar_x + max(share * scale, 0.04) / 2, y)
        )
        bars.append(
            scene.geometry.fill_level(
                mask,
                BRICK if lead else "#CFC8BC",
                0,
                direction="right",
                keep_outline=False,
            )
        )
        rows.append(
            t(
                scene,
                f"{share:.1f} %",
                bar_x + share * scale + 0.14,
                y,
                font=MONO,
                size=0.19,
                color=BRICK_DEEP if lead else MUTED,
                anchor=Anchor.LEFT,
            )
        )
    scene.play(title.animate.fade_in().duration(0.4))
    scene.play(
        stagger(
            *[
                sequence(
                    rows[2 * i].animate.fade_in().duration(0.25),
                    bars[i].animate.fill_level(1).duration(0.5),
                    rows[2 * i + 1].animate.fade_in().duration(0.2),
                )
                for i in range(len(bars))
            ],
            each=0.09,
        )
    )
    source(
        scene,
        f"{SOURCE_LABEL} · Características de la vivienda (VIV6). "
        "El material de las paredes no acredita confinamiento ni desempeño sísmico.",
    )
    scene.stop("materiales-listo")


def _brick_wall(scene: Scene, cx: float, cy: float, width: float, height: float):
    """Muro confinado en elevación: ladrillos en soga, columnas dentadas y solera."""
    col_w, beam_h = 0.36, 0.3
    brick_w, brick_h, joint = 0.40, 0.13, 0.035
    left = cx - width / 2 + col_w
    right = cx + width / 2 - col_w
    bottom = cy - height / 2
    rows: list[Drawable] = []
    n_rows = int((height - beam_h) / (brick_h + joint))
    tooth = 0.07
    for r in range(n_rows):
        y = bottom + joint / 2 + brick_h / 2 + r * (brick_h + joint)
        # El dentado: cada dos hiladas el ladrillo extremo entra en la columna.
        toothed = (r // 2) % 2 == 0
        x0 = left - (tooth if toothed else 0)
        x1 = right + (tooth if toothed else 0)
        x = x0 - (brick_w / 2 if r % 2 else 0)
        bricks: list[Drawable] = []
        while x < x1 - 0.02:
            a, b = max(x, x0), min(x + brick_w, x1)
            if b - a > 0.05:
                bricks.append(
                    scene.geometry.rect(b - a - joint, brick_h)
                    .fill(BRICK)
                    .no_stroke()
                    .move_to((a + b) / 2, y)
                )
            x += brick_w
        rows.append(scene.geometry.group(bricks))
    top_bricks = bottom + n_rows * (brick_h + joint)

    def column(x_in: float, x_out: float) -> Drawable:
        pts = [(x_out, bottom), (x_out, top_bricks)]
        sign = 1 if x_in > x_out else -1
        for r in reversed(range(n_rows)):
            y1 = bottom + (r + 1) * (brick_h + joint)
            y0 = bottom + r * (brick_h + joint)
            toothed = (r // 2) % 2 == 0
            xi = x_in - sign * tooth if toothed else x_in
            pts += [(xi, y1), (xi, y0)]
        return scene.geometry.polygon(pts).fill(CONCRETE_SOFT).stroke(CONCRETE, 0.012)

    columns = [column(left, left - col_w), column(right, right + col_w)]
    beam = (
        scene.geometry.rect(width, beam_h)
        .fill(CONCRETE_SOFT)
        .stroke(CONCRETE, 0.012)
        .move_to(cx, top_bricks + beam_h / 2)
    )
    ground = scene.geometry.line(
        cx - width / 2 - 0.4, bottom, cx + width / 2 + 0.4, bottom
    ).stroke(INK_SOFT, 0.02)
    hatch = [
        scene.geometry.line(x, bottom, x - 0.14, bottom - 0.14).stroke(MUTED, 0.01)
        for x in [
            cx - width / 2 - 0.3 + 0.22 * i for i in range(int((width + 0.8) / 0.22))
        ]
    ]
    return rows, columns, beam, scene.geometry.group([ground, *hatch]), top_bricks


def seismic(scene: Scene) -> None:
    header(scene, KICKER, "En un país sísmico, el muro confinado trabaja como unidad")

    plates = scene.media.lottie("placas_subduccion.lottie")
    plates.scale_by(0.43).move_to(-5.0, 0.4)
    plate_caption = t(
        scene,
        "Subducción de la placa de Nazca\nbajo la placa Sudamericana",
        -5.0,
        -1.55,
        size=0.2,
        color=INK_SOFT,
        anchor=Anchor.TOP,
    )
    scene.play(sequence(plates.animate.fade_in().duration(0.5), plates))
    scene.play(plate_caption.animate.fade_in().duration(0.4))
    scene.stop("contexto-sismico")

    cx, cy, w, h = 1.15, -0.2, 3.7, 3.2
    rows, columns, beam, ground, top_bricks = _brick_wall(scene, cx, cy, w, h)
    scene.play(ground.animate.create().duration(0.5))
    scene.play(
        stagger(
            *[
                r.animate.fade_in_from(Direction.DOWN, 0.05).duration(0.25)
                for r in rows
            ],
            each=0.045,
        )
    )
    wall_note = _callout(
        scene,
        "Muro de ladrillo",
        "se asienta primero,\ncon los extremos dentados",
        (cx + 0.7, cy - 0.5),
        (3.75, -0.75),
    )
    scene.play(wall_note)
    fills = [
        scene.geometry.fill_level(
            c, CONCRETE_SOFT, 0, direction="up", keep_outline=True
        )
        for c in columns
    ]
    scene.play([f.animate.fill_level(1).duration(0.9) for f in fills])
    beam_fill = scene.geometry.fill_level(
        beam, CONCRETE_SOFT, 0, direction="right", keep_outline=True
    )
    scene.play(beam_fill.animate.fill_level(1).duration(0.6))
    col_note = _callout(
        scene,
        "Columnas y viga solera",
        "se vacían después y\nconfinan el muro",
        (cx + w / 2 - 0.18, top_bricks - 0.6),
        (3.75, 1.2),
    )
    scene.play(col_note)
    force = (
        scene.geometry.arrow(
            cx - w / 2 - 1.2,
            top_bricks + 0.15,
            cx - w / 2 - 0.08,
            top_bricks + 0.15,
            head_length=0.2,
            head_width=0.2,
            body_width=0.05,
        )
        .fill(STEEL)
        .no_stroke()
    )
    force_label = t(
        scene,
        "V sísmico",
        cx - w / 2 - 1.2,
        top_bricks + 0.32,
        size=0.2,
        color=STEEL,
        weight=700,
        anchor=Anchor.BOTTOM_LEFT,
    )
    scene.play(
        [
            force.animate.grow_arrow().duration(0.5),
            force_label.animate.fade_in().duration(0.4),
        ]
    )
    takeaway(
        scene,
        "La E.070 exige densidad mínima de muros en ambas direcciones y buena conexión",
    )
    source(
        scene,
        "Tesis · cap. 1, Problemática; cap. 2, Albañilería confinada (Gonzales, 1992; Tavera, 2014; San Bartolomé, 2018)",
    )
    scene.stop("muro-confinado")


def _callout(
    scene: Scene,
    title: str,
    body: str,
    target: tuple[float, float],
    anchor: tuple[float, float],
    *,
    align_right: bool = False,
):
    ax, ay = anchor
    dot = scene.geometry.circle(0.05).fill(INK).no_stroke().move_to(*target)
    lead = scene.geometry.line(target, (ax, ay - 0.16)).stroke(INK_SOFT, 0.01)
    head = t(
        scene,
        title,
        ax,
        ay,
        size=0.22,
        weight=900,
        color=INK,
        anchor=Anchor.BOTTOM_RIGHT if align_right else Anchor.BOTTOM_LEFT,
    )
    sub = t(
        scene,
        body,
        ax,
        ay - 0.05,
        size=0.18,
        color=INK_SOFT,
        anchor=Anchor.TOP_RIGHT if align_right else Anchor.TOP_LEFT,
    )
    return stagger(
        dot.animate.grow_from_center().duration(0.25),
        lead.animate.create().duration(0.35),
        head.animate.fade_in().duration(0.3),
        sub.animate.fade_in().duration(0.3),
        each=0.12,
    )


def manual_transfer(scene: Scene) -> None:
    header(scene, KICKER, "ETABS no verifica la E.070: los datos se trasladan a mano")

    # Ventana de resultados del modelo: valores reales de V_e, piso 1, MCT (tb:agriet_xy).
    piers = ["X1", "X3", "X4", "X5", "X6"]
    etabs = _window(scene, -5.15, 0.85, 3.9, 2.75, "ETABS · Pier Forces")
    head = ["Story", "Pier", "Ve (tonf)"]
    xs = [-6.8, -5.6, -4.3]
    table: list[Drawable] = [
        t(
            scene,
            h_,
            x,
            1.55,
            font=MONO,
            size=0.15,
            weight=700,
            color=INK_SOFT,
            anchor=Anchor.LEFT,
        )
        for h_, x in zip(head, xs, strict=True)
    ]
    records: list[list[Drawable]] = []
    for i, pier in enumerate(piers):
        y = 1.15 - i * 0.36
        cells: list[Drawable] = [
            t(
                scene,
                "Story1",
                xs[0],
                y,
                font=MONO,
                size=0.16,
                color=INK,
                anchor=Anchor.LEFT,
            ),
            t(
                scene,
                pier,
                xs[1],
                y,
                font=MONO,
                size=0.16,
                color=INK,
                anchor=Anchor.LEFT,
            ),
            t(
                scene,
                f"{CRACKING_FLOOR1['MCT'][pier][0]:.3f}",
                xs[2],
                y,
                font=MONO,
                size=0.16,
                color=INK,
                anchor=Anchor.LEFT,
            ),
        ]
        records.append(cells)
    sheet = _window(
        scene, 4.4, 0.85, 4.6, 2.75, "Hoja de cálculo · E.070", tint=PASS_TINT
    )
    letters = [
        t(
            scene,
            c,
            2.55 + i * 1.2,
            1.55,
            font=MONO,
            size=0.14,
            color=MUTED,
            anchor=Anchor.CENTER,
        )
        for i, c in enumerate("ABCD")
    ]
    grid = [
        scene.geometry.line(2.2, 1.35 - j * 0.36, 6.6, 1.35 - j * 0.36).stroke(
            FAINT, 0.01
        )
        for j in range(6)
    ] + [
        scene.geometry.line(
            2.2 + i * 1.2 - 0.05, 1.4, 2.2 + i * 1.2 - 0.05, -0.45
        ).stroke(FAINT, 0.01)
        for i in range(1, 4)
    ]
    scene.play(
        [
            etabs.animate.fade_in().duration(0.4),
            *[x.animate.fade_in().duration(0.4) for x in table],
        ]
    )
    scene.play(
        stagger(
            *[c.animate.fade_in().duration(0.2) for row in records for c in row],
            each=0.02,
        )
    )
    scene.play(
        [
            sheet.animate.fade_in().duration(0.4),
            *[x.animate.fade_in().duration(0.4) for x in letters + grid],
        ]
    )

    steps = [("exportar", -2.25), ("filtrar", -0.6), ("copiar", 1.05)]
    step_labels = [
        pill(
            scene,
            name,
            x,
            1.72,
            color=BRICK_DEEP,
            background=BRICK_SOFT,
            size=0.17,
            font=MONO,
        )
        for name, x in steps
    ]
    arrow = (
        scene.geometry.arrow(
            -3.0, 1.3, 1.9, 1.3, head_length=0.18, head_width=0.16, body_width=0.03
        )
        .fill(BRICK)
        .no_stroke()
    )
    scene.play(
        stagger(
            arrow.animate.grow_arrow().duration(0.4),
            *[p.animate.fade_in().duration(0.25) for p in step_labels],
            each=0.12,
        )
    )
    # Cada fila viaja de la tabla del modelo a la hoja; es la misma cifra, trasladada.
    moves = []
    for i, row in enumerate(records):
        y = 1.15 - i * 0.36
        copies = [
            t(
                scene,
                "1",
                2.55,
                y,
                font=MONO,
                size=0.16,
                color=INK,
                anchor=Anchor.CENTER,
            ),
            t(
                scene,
                piers[i],
                3.75,
                y,
                font=MONO,
                size=0.16,
                color=INK,
                anchor=Anchor.CENTER,
            ),
            t(
                scene,
                f"{CRACKING_FLOOR1['MCT'][piers[i]][0]:.3f}",
                4.95,
                y,
                font=MONO,
                size=0.16,
                color=INK,
                anchor=Anchor.CENTER,
            ),
        ]
        moves.append(
            sequence(
                *[r.animate.indicate().duration(0.3) for r in row[1:2]],
                *[
                    c.animate.fade_in_from(Direction.LEFT, 0.5).duration(0.35)
                    for c in copies
                ],
            )
        )
    scene.play(stagger(*moves, each=0.35))
    risks = [
        ("¿fila y Pier correctos?", -0.55, 0.65),
        ("¿combinación de carga?", -0.55, 0.15),
        ("¿unidades y signos?", -0.55, -0.35),
    ]
    risk_pills = [
        pill(
            scene,
            r,
            x,
            y,
            color=INK_SOFT,
            background=CARD,
            border=RULE,
            size=0.17,
            font="Lato",
        )
        for r, x, y in risks
    ]
    scene.play(
        stagger(
            *[
                p.animate.fade_in_from(Direction.UP, 0.08).duration(0.35)
                for p in risk_pills
            ],
            each=0.12,
        )
    )
    scene.stop("traslado-manual")

    loop = (
        scene.geometry.curved_arrow(
            4.4,
            -0.6,
            -5.15,
            -0.6,
            -0.3,
            head_length=0.16,
            head_width=0.16,
            body_width=0.028,
        )
        .fill(BRICK)
        .no_stroke()
    )
    loop_label = t(
        scene,
        "Si un muro no cumple: modificar el modelo, reanalizar y repetir el traslado",
        -0.4,
        -1.35,
        size=0.21,
        color=BRICK_DEEP,
        anchor=Anchor.TOP,
    )
    scene.play(
        [
            loop.animate.grow_arrow().duration(0.9),
            loop_label.animate.fade_in().duration(0.5),
        ]
    )
    question = panel(
        scene, 0, -2.55, 14.6, 0.8, fill=PAPER_DEEP, border=None, radius=0.14
    )
    q_text = t(
        scene,
        "¿Cómo sistematizar la verificación E.070 a partir del modelo de ETABS?",
        0,
        -2.55,
        font=DISPLAY,
        size=0.3,
        weight=700,
        color=INK,
        anchor=Anchor.CENTER,
    )
    scene.play(
        [
            question.animate.fade_in().duration(0.4),
            q_text.animate.fade_in_from(Direction.UP, 0.08).duration(0.6),
        ]
    )
    source(
        scene,
        "Tesis · cap. 1, Problemática y Justificación. Valores: $V_e$ del piso 1, MCT (tb:agriet_xy).",
    )
    scene.stop("pregunta-de-investigacion")


PASS_TINT = STEEL_SOFT


def _window(
    scene: Scene, cx: float, cy: float, w: float, h: float, title: str, *, tint=CARD
) -> Drawable:
    frame = (
        scene.geometry.rounded_rect(w, h, 0.1)
        .fill(CARD)
        .stroke(RULE, 0.014)
        .move_to(cx, cy)
    )
    bar = (
        scene.geometry.rounded_rect(w, 0.34, 0.1)
        .fill(tint)
        .no_stroke()
        .move_to(cx, cy + h / 2 - 0.17)
    )
    dots = [
        scene.geometry.circle(0.045)
        .fill(c)
        .no_stroke()
        .move_to(cx - w / 2 + 0.2 + i * 0.15, cy + h / 2 - 0.17)
        for i, c in enumerate([BRICK, "#D9B25B", "#9DB08A"])
    ]
    name = t(
        scene,
        title,
        cx - w / 2 + 0.6,
        cy + h / 2 - 0.17,
        font=MONO,
        size=0.14,
        color=INK_SOFT,
        anchor=Anchor.LEFT,
    )
    return scene.geometry.group([frame, bar, *dots, name])


SECTION = Section(
    "problematica",
    [
        SectionStep(
            name="Problemática · material",
            build=materials,
            transition=Transition.cross_fade(0.45),
            notes=(
                "45 s. INEI, Censos Nacionales 2025, viviendas particulares con ocupantes: "
                "61.8 % declara paredes de ladrillo o bloque de concreto (la tesis citaba INEI "
                "2017; se actualizó el dato). Aclarar que el material no acredita confinamiento "
                "ni desempeño: solo muestra la relevancia del sistema. El relleno del mapa es "
                "ilustrativo, no una distribución geográfica."
            ),
        ),
        SectionStep(
            name="Problemática · sistema sísmico",
            build=seismic,
            transition=Transition.cross_fade(0.45),
            notes=(
                "1 min. Perú en el Cinturón de Fuego (Tavera, 2014). La albañilería confinada "
                "llegó tras el terremoto de Lima de 1940. Explicar el proceso: primero el muro con "
                "extremos dentados, después se vacían columnas y viga solera; el conjunto trabaja "
                "como una unidad y gana ductilidad (Gonzales, 1992). Por eso la E.070 pide densidad "
                "mínima de muros en ambas direcciones y conexión con los confinamientos."
            ),
        ),
        SectionStep(
            name="Problemática · traslado manual",
            build=manual_transfer,
            transition=Transition.cross_fade(0.45),
            notes=(
                "1.25 min. Los programas comerciales (ETABS, SAP2000) no implementan la E.070; el "
                "ingeniero exporta tablas, filtra, copia a hojas de cálculo y verifica. Las cifras "
                "son V_e reales del piso 1 del modelo MCT (tb:agriet_xy), usadas solo para ilustrar "
                "el traslado. Riesgos citados en la tesis: errores de selección, transcripción, "
                "ordenamiento y verificaciones omitidas; no se midió su frecuencia. Cerrar con la "
                "pregunta de investigación."
            ),
        ),
    ],
)
