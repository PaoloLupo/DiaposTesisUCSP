"""Portada: título de la tesis y la planta del caso dibujándose."""

from gaanim import Anchor, Direction, Scene, stagger

from tesis.building import DEPTH, WIDTH, draw_plan, grow_walls
from tesis.kit import LEFT_EDGE, dimension, label, t
from tesis.theme import BRICK, DISPLAY, INK, INK_SOFT, MONO, MUTED

NOTES = (
    "45 s. Saludo al jurado. Presentar a los autores y al asesor. "
    "Enunciar en una frase el problema: la verificación E.070 de una distribución "
    "de muros se hace a mano con hojas de cálculo, y la tesis propone un marco de "
    "trabajo para sistematizarla con un programa conectado a ETABS (Alba). "
    "La planta que se dibuja es el caso de estudio de San Bartolomé (2006), el mismo "
    "edificio que acompaña toda la exposición. Título según TesisUCSP/main.typ (d1d0b73)."
)


def build(scene: Scene) -> None:
    _ = scene.segment("Portada", notes=NOTES)

    logo = scene.media.svg("logoucsp.svg").scale_to(0.00072).fill(INK)
    logo.move_to(LEFT_EDGE + 0.2, 3.72)
    university = label(
        scene,
        "Universidad Católica San Pablo",
        LEFT_EDGE + 0.55,
        3.93,
        color=INK,
        size=0.16,
    )
    school = t(
        scene,
        "Escuela Profesional de Ingeniería Civil",
        LEFT_EDGE + 0.55,
        3.65,
        size=0.17,
        color=MUTED,
    )

    # Retícula: universidad arriba; título y planta en la banda central, con la
    # fila de ejes de la planta a la altura del kicker; créditos abajo a la izquierda.
    kicker = label(
        scene,
        "Tesis para optar el título profesional de Ingeniero Civil",
        LEFT_EDGE,
        2.55,
        color=BRICK,
        size=0.15,
    )
    title = t(
        scene,
        # Seis líneas por unidades de sentido: el título llena el alto de la
        # columna, desde el rótulo hasta los créditos, sin invadir la planta.
        "Marco de trabajo para\nla automatización\ndel diseño de la\n"
        "distribución de muros\nen planta para edificios\nde albañilería confinada",
        LEFT_EDGE,
        2.2,
        font=DISPLAY,
        size=0.63,
        weight=700,
        color=INK,
    )

    plan = draw_plan(scene, (4.0, 0.5), 5.95, drawn_thickness=0.075)
    ox, oy = plan.origin
    s = plan.scale

    # Créditos apilados bajo el título y anclados al margen inferior: autores,
    # asesor y, sin rótulo, ciudad y año.
    credits = [
        t(
            scene,
            "Paolo Cesar Guillen Lupo  ·  Pamela Lucyla Banda Alarta",
            LEFT_EDGE,
            -2.35,
            size=0.29,
            weight=700,
            color=INK,
        ),
        t(
            scene,
            "Asesor: Mgtr. David Miguel Chalco Pari",
            LEFT_EDGE,
            -2.9,
            size=0.23,
            color=INK_SOFT,
        ),
        t(scene, "Arequipa, 2026", LEFT_EDGE, -3.3, size=0.21, color=MUTED),
    ]
    dims = [
        dimension(
            scene, (ox, oy), (ox + WIDTH * s, oy), "16.60 m", side="below", offset=0.4
        ),
        dimension(
            scene,
            (ox + WIDTH * s, oy),
            (ox + WIDTH * s, oy + DEPTH * s),
            "8.00 m",
            side="right",
            offset=0.28,
        ),
    ]
    caption = t(
        scene,
        "Caso de estudio · San Bartolomé (2006) · planta típica, 4 pisos",
        ox + WIDTH * s / 2,
        -1.95,
        font=MONO,
        size=0.14,
        color=MUTED,
        anchor=Anchor.TOP,
    )

    scene.play(
        stagger(
            stagger(
                logo.animate.fade_in().duration(0.5),
                university.animate.fade_in().duration(0.5),
                school.animate.fade_in().duration(0.5),
                each=0.08,
            ),
            kicker.animate.fade_in_from(Direction.RIGHT, 0.12).duration(0.5),
            title.animate.reveal(style="slide_up", by="line", stagger=0.08).duration(1.1),
            stagger(*[c.animate.fade_in().duration(0.5) for c in credits], each=0.06),
            each=0.18,
        )
    )
    scene.play(
        stagger(
            stagger(*[g.animate.create().duration(0.6) for g in plan.grid], each=0.04),
            stagger(
                *[b.animate.fade_in().duration(0.3) for b in plan.bubbles], each=0.03
            ),
            plan.slab.animate.fade_in().duration(0.6),
            plan.void.animate.fade_in().duration(0.4),
            grow_walls(plan.all_walls, total=1.1, duration=0.45),
            stagger(*[d.animate.create().duration(0.5) for d in dims], each=0.1),
            caption.animate.fade_in().duration(0.4),
            each=0.25,
        )
    )
    scene.stop("portada")
