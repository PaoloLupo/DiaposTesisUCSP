"""Divisores tipo agenda y riel de avance persistente.

Cada bloque abre con una diapositiva que muestra su número, su pregunta guía y
la agenda completa; el marcador terracota se desplaza desde el bloque anterior.
El riel inferior es HUD: persiste entre segmentos y avanza con cada escena.

El divisor es el primer paso de la sección, así que ``gaanim . --sections
resultados`` o ``--from resultados`` también lo incluyen.
"""

from gaanim import (
    Anchor,
    Direction,
    Drawable,
    Easing,
    NavigationEntry,
    Playable,
    ProgressRail,
    Scene,
    Section,
    SectionProgress,
    SectionStep,
    TextStyle,
    Transition,
    stagger,
)

from tesis.kit import LEFT_EDGE, RIGHT_EDGE, t
from tesis.theme import (
    BRICK,
    DISPLAY,
    FAINT,
    INK,
    INK_SOFT,
    MONO,
    MUTED,
    RULE,
    SANS,
)

# Clave, título de la agenda, pregunta guía y rótulo del riel.
SECTIONS = (
    (
        "problematica",
        "Problemática",
        "¿Por qué importa verificar la distribución de muros?",
        "Problemática",
    ),
    (
        "objetivos",
        "Objetivos y método",
        "¿Qué se propuso y cómo se evaluó?",
        "Objetivos",
    ),
    (
        "fundamentos",
        "Fundamentos",
        "¿Qué exige la norma a una distribución de muros?",
        "Fundamentos",
    ),
    (
        "manual",
        "Proceso manual",
        "¿Cómo se verifica hoy un edificio de albañilería?",
        "Proceso manual",
    ),
    (
        "marco",
        "Marco de trabajo",
        "¿Qué se automatiza y con qué lógica?",
        "Marco de trabajo",
    ),
    (
        "alba",
        "Implementación: Alba",
        "¿Cómo se conecta el marco con ETABS?",
        "Alba",
    ),
    (
        "resultados",
        "Resultados",
        "¿Qué muestran los tres modelos del caso?",
        "Resultados",
    ),
    (
        "conclusiones",
        "Conclusiones",
        "¿Qué aporta el trabajo y qué queda abierto?",
        "Conclusiones",
    ),
)
KEYS = tuple(key for key, _, _, _ in SECTIONS)

AGENDA_X = 1.9
AGENDA_TOP = 2.35
AGENDA_GAP = 0.66
RAIL_Y = -4.46
# Sello: el escudo de la UCSP, pequeño y en gris, sobre el kicker de cada escena.
SEAL_Y = 4.24
# Número de lámina: a la derecha, en la línea de la fuente, para que el jurado
# pueda pedir «vuelva a la lámina 23».
NUMBER_Y = -3.72
# Escenas que no llevan sello ni número (el cierre repite la portada).
UNNUMBERED = {"Cierre"}


def _agenda_row(scene: Scene, entry: NavigationEntry, state: str) -> Drawable:
    """Número en mono y nombre; el bloque actual en terracota y negrita."""
    current = state == "current"
    color = BRICK if current else (INK_SOFT if state == "done" else MUTED)
    number = t(
        scene,
        f"{entry.index + 1:02d}",
        0,
        0,
        font=MONO,
        size=0.2,
        color=color,
        anchor=Anchor.LEFT,
    )
    name = t(
        scene,
        entry.title,
        0.65,
        0,
        font=SANS,
        size=0.3,
        weight=900 if current else 400,
        color=INK if current else color,
        anchor=Anchor.LEFT,
    )
    return scene.geometry.group([number, name])


class SectionIndex:
    """Reutiliza una instancia por escena; ``build`` abre divisor y contenido."""

    def __init__(self, scene: Scene):
        self.scene = scene
        self._previous: int | None = None
        self._rail: ProgressRail | None = None
        self._seal: Drawable | None = None
        self._seal_visible = False
        self._slide = 0

    def build(self, section: Section, *, transition: Transition | None = None) -> None:
        if section.key not in KEYS:
            raise ValueError(
                f"Bloque desconocido {section.key!r}; opciones: {', '.join(KEYS)}"
            )
        active = KEYS.index(section.key)
        _, title, question, _ = SECTIONS[active]
        divider = SectionStep(
            name="Índice",
            build=lambda scene: self._divider(scene, active),
            # Cambio de capítulo: un barrido suave hacia la izquierda; dentro de
            # cada bloque las diapositivas siguen con fundido cruzado.
            transition=transition
            or Transition.wipe(0.6, direction="left", feather=0.2, easing=Easing.SMOOTH),
            notes=(
                f"Bloque {active + 1} de {len(SECTIONS)}: {title}. "
                f"Pregunta guía: {question} Transición breve, 5-10 s."
            ),
        )
        Section(section.key, [divider, *section.steps], title=title).build(
            self.scene, on_enter=self._advance
        )
        self._previous = active

    def _divider(self, scene: Scene, active: int) -> None:
        previous = self._previous
        _, title, question, _ = SECTIONS[active]
        _ = scene.camera.reset()
        rail = self._rail or self._build_rail()
        self._set_seal(False)

        # El numeral rueda desde el bloque anterior hasta el actual.
        numeral = scene.viz.rolling_number(
            (previous if previous is not None else active) + 1,
            min_digits=2,
            font_family=DISPLAY,
            weight=700,
            font_size=1.55,
            color=BRICK,
        ).move_to(LEFT_EDGE, 1.3, Anchor.BOTTOM_LEFT)
        heading = t(
            scene,
            title,
            LEFT_EDGE,
            0.95,
            font=DISPLAY,
            size=0.78,
            weight=700,
            color=INK,
        )
        prompt = t(scene, question, LEFT_EDGE, -0.05, size=0.34, color=INK_SOFT)
        divider = scene.geometry.line(1.35, 2.7, 1.35, -3.0).stroke(RULE, 0.012)

        agenda = scene.sections.agenda(
            [(key, name) for key, name, _, _ in SECTIONS],
            previous if previous is not None else active,
            pitch=AGENDA_GAP,
            item=_agenda_row,
            # Única marca vertical de la presentación: señala el bloque actual.
            marker=lambda scene: (
                scene.geometry.rect(0.07, 0.42).fill(BRICK).no_stroke()
            ),
        )
        agenda.root.shift_by(AGENDA_X, AGENDA_TOP)

        scene.play(
            stagger(
                numeral.visual.animate.fade_in().duration(0.4),
                heading.animate.reveal(style="slide_up", by="word", stagger=0.06)
                .duration(0.7),
                prompt.animate.fade_in().duration(0.5),
                divider.animate.create().duration(0.5),
                agenda.root.animate.fade_in().duration(0.4),
                each=0.08,
            )
        )
        animations: list[Playable] = [
            agenda.animate.focus(active, easing=Easing.SMOOTH_SPRING),
            rail.animate.enter(active),
        ]
        if previous is not None:
            animations.append(numeral.count_to(active + 1, duration=0.7))
        scene.play(animations, duration=0.7)
        scene.stop(f"entrada-{KEYS[active]}")

    def _build_rail(self) -> ProgressRail:
        scene = self.scene
        rail = scene.sections.progress_rail(
            [(key, label.upper()) for key, _, _, label in SECTIONS],
            length=16 - 2 * 0.7,
            thickness=0.04,
            segmented=True,
            track=lambda scene, w, h: scene.geometry.rect(w, h).fill(FAINT).no_stroke(),
            fill_color=BRICK,
            captions=True,
            caption_style=TextStyle(font=SANS, size=0.13, weight=900),
            caption_colors={"done": MUTED, "current": BRICK, "upcoming": MUTED},
        )
        rail.root.shift_by(0, RAIL_Y).hud().z_index(100)
        scene.persist(rail.root)
        scene.play(rail.root.animate.fade_in(), duration=0.35)
        self._rail = rail
        return rail

    def _advance(self, scene: Scene, progress: SectionProgress) -> None:
        """Al entrar a cada escena el riel avanza y aparece su número (el divisor no cuenta)."""
        if progress.index == 1 or self._rail is None:
            return
        numbered = progress.step.name not in UNNUMBERED
        self._set_seal(numbered)
        active = KEYS.index(progress.key)
        share = (progress.index - 1) / (progress.total - 1)
        animations: list[Playable] = [
            self._rail.animate.to((active + share) / len(SECTIONS))
        ]
        if numbered:
            self._slide += 1
            number = t(
                scene,
                f"{self._slide:02d}",
                RIGHT_EDGE,
                NUMBER_Y,
                font=MONO,
                size=0.17,
                color=MUTED,
                anchor=Anchor.TOP_RIGHT,
            )
            animations.append(number.animate.fade_in())
        scene.play(animations, duration=0.35)

    def _set_seal(self, visible: bool) -> None:
        """Muestra el escudo en las escenas y lo oculta en los divisores y el cierre."""
        if visible == self._seal_visible:
            return
        scene = self.scene
        if self._seal is None:
            seal = (
                scene.media.svg("logoucsp.svg")
                .scale_to(0.033)
                .fill(MUTED)
                .move_to(LEFT_EDGE + 0.09, SEAL_Y)
            )
            seal.hud().z_index(100)
            scene.persist(seal)
            self._seal = seal
        anim = self._seal.animate.fade_in() if visible else self._seal.animate.fade_out()
        scene.play(anim, duration=0.3)
        self._seal_visible = visible
