"""Portada: título de la tesis y la planta del caso dibujándose."""

from gaanim import Anchor, Direction, Scene, stagger

from tesis.building import DEPTH, WIDTH, draw_plan
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

    kicker = label(
        scene,
        "Tesis para optar el título profesional de Ingeniero Civil",
        LEFT_EDGE,
        2.45,
        color=BRICK,
        size=0.15,
    )
    title = t(
        scene,
        "Marco de trabajo para la\nautomatización del diseño de la\n"
        "distribución de muros en planta\npara edificios de albañilería\nconfinada",
        LEFT_EDGE,
        2.1,
        font=DISPLAY,
        size=0.5,
        weight=700,
        color=INK,
    )
    rule = scene.geometry.line(LEFT_EDGE, -1.02, LEFT_EDGE + 1.1, -1.02).stroke(
        BRICK, 0.04
    )
    authors = t(
        scene,
        "Paolo Cesar Guillen Lupo\nPamela Lucyla Banda Alarta",
        LEFT_EDGE,
        -1.3,
        size=0.29,
        weight=700,
        color=INK,
    )
    advisor = t(
        scene,
        "Asesor: Mgtr. David Miguel Chalco Pari",
        LEFT_EDGE,
        -2.2,
        size=0.22,
        color=INK_SOFT,
    )
    place = t(scene, "Arequipa, 2026", LEFT_EDGE, -2.62, size=0.2, color=MUTED)

    plan = draw_plan(scene, (3.95, 0.35), 6.1, drawn_thickness=0.075)
    ox, oy = plan.origin
    s = plan.scale
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
            offset=0.4,
        ),
    ]
    caption = t(
        scene,
        "Caso de estudio · San Bartolomé (2006) · planta típica, 4 pisos",
        3.95,
        -2.3,
        font=MONO,
        size=0.14,
        color=MUTED,
        anchor=Anchor.TOP,
    )

    walls_x = [plan.walls[n] for n in plan.walls if n.startswith("X")]
    walls_y = [plan.walls[n] for n in plan.walls if n.startswith("Y")]
    scene.play(
        stagger(
            stagger(
                logo.animate.fade_in().duration(0.5),
                university.animate.fade_in().duration(0.5),
                school.animate.fade_in().duration(0.5),
                each=0.08,
            ),
            kicker.animate.fade_in_from(Direction.RIGHT, 0.12).duration(0.5),
            title.animate.fade_in_from(Direction.UP, 0.12).duration(0.9),
            rule.animate.create().duration(0.5),
            stagger(
                authors.animate.fade_in().duration(0.5),
                advisor.animate.fade_in().duration(0.5),
                place.animate.fade_in().duration(0.5),
                each=0.1,
            ),
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
            stagger(
                *[w.animate.grow_from_center().duration(0.45) for w in walls_x],
                each=0.05,
            ),
            stagger(
                *[w.animate.grow_from_center().duration(0.45) for w in walls_y],
                each=0.05,
            ),
            stagger(*[d.animate.create().duration(0.5) for d in dims], each=0.1),
            caption.animate.fade_in().duration(0.4),
            each=0.25,
        )
    )
    scene.stop("portada")
