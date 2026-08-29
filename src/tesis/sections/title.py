from gaanim import BLACK, Scene

from tesis.theme import ACCENT


def build(scene: Scene):
    _ = scene.segment("Titulo")
    logo = scene.media.svg("logoucsp.svg").scale_to(0.0013).move_to(0, 3.7).fill(BLACK)
    faculty = scene.text(
        "*UNIVERSIDAD CATÓLICA SAN PABLO*\nFacultad de Arquitectura, Computación e Ingenierías\nEscuela Profesional de Ingeniería Civil",
        text_align="center",
        line_spacing=1.4,
    ).move_to(0, 2.4)
    title = scene.text(
        "*MARCO DE TRABAJO PARA LA AUTOMATIZACIÓN DEL DISEÑO DE LA DISTRIBUCIÓN DE MUROS EN PLANTA PARA EDIFICIOS DE ALBAÑILERÍA CONFINADA*",
        role="title",
        text_align="center",
        line_spacing=1.35,
    )
    title_accent = scene.geometry.line(-7.2, -1.8, 7.2, -1.8).stroke(ACCENT, 0.05)

    authors = scene.text(
        "Paolo Cesar Guillen Lupo  •  Pamela Lucyla Banda Alarta\n*Asesor:* Mgtr. David Miguel Chalco Pari",
        text_align="center",
        line_spacing=1.8,
    ).move_to(0, -2.6)


    scene.play(
        [
            logo.animate.fade_in(),
            faculty.animate.fade_in(),
            title.animate.write(),
            title_accent.animate.create(),
            authors.animate.fade_in(),
        ]
    )

    scene.stop()
