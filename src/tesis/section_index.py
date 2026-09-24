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
    Playable,
    NavigationEntry,
    ProgressRail,
    Scene,
    Section,
    SectionProgress,
    SectionStep,
    TextStyle,
    Transition,
    stagger,
)

from tesis.kit import LEFT_EDGE, t
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
            transition=transition or Transition.cross_fade(0.45),
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
        prompt_rule = scene.geometry.line(
            LEFT_EDGE, -0.72, LEFT_EDGE + 1.2, -0.72
        ).stroke(BRICK, 0.035)
        divider = scene.geometry.line(1.35, 2.7, 1.35, -3.0).stroke(RULE, 0.012)

        agenda = scene.sections.agenda(
            [(key, name) for key, name, _, _ in SECTIONS],
            previous if previous is not None else active,
            pitch=AGENDA_GAP,
            item=_agenda_row,
            marker=lambda scene: scene.geometry.rounded_rect(0.07, 0.42, 0.035)
            .fill(BRICK)
            .no_stroke(),
        )
        agenda.root.shift_by(AGENDA_X, AGENDA_TOP)

        scene.play(
            stagger(
                numeral.visual.animate.fade_in().duration(0.4),
                heading.animate.fade_in_from(Direction.UP, 0.12).duration(0.6),
                prompt.animate.fade_in().duration(0.5),
                prompt_rule.animate.create().duration(0.5),
                divider.animate.create().duration(0.5),
                agenda.root.animate.fade_in().duration(0.4),
                each=0.08,
            )
        )
        animations: list[Playable] = [
            agenda.animate.focus(active),
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
            caption_style=TextStyle(font=SANS, size=0.115, weight=900),
            caption_colors={"done": MUTED, "current": BRICK, "upcoming": MUTED},
        )
        rail.root.shift_by(0, RAIL_Y).hud().z_index(100)
        scene.persist(rail.root)
        scene.play(rail.root.animate.fade_in(), duration=0.35)
        self._rail = rail
        return rail

    def _advance(self, scene: Scene, progress: SectionProgress) -> None:
        """Al entrar a cada escena el tramo activo del riel avanza (el divisor no cuenta)."""
        if progress.index == 1 or self._rail is None:
            return
        active = KEYS.index(progress.key)
        share = (progress.index - 1) / (progress.total - 1)
        scene.play(
            self._rail.animate.to((active + share) / len(SECTIONS)), duration=0.35
        )
