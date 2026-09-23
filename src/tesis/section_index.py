"""Divisores tipo agenda y riel de avance persistente.

Cada bloque abre con una diapositiva que muestra su número, su pregunta guía y
la agenda completa; el marcador terracota se desplaza desde el bloque anterior.
El riel inferior es HUD: persiste entre segmentos y avanza con cada escena.
"""

from gaanim import (
    Anchor,
    Direction,
    Drawable,
    Scene,
    Section,
    SectionProgress,
    Text,
    Transition,
    parallel,
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

SECTIONS = (
    (
        "problematica",
        "Problemática",
        "¿Por qué importa verificar la distribución de muros?",
    ),
    ("objetivos", "Objetivos y método", "¿Qué se propuso y cómo se evaluó?"),
    ("fundamentos", "Fundamentos", "¿Qué exige la norma a una distribución de muros?"),
    ("manual", "Proceso manual", "¿Cómo se verifica hoy un edificio de albañilería?"),
    ("marco", "Marco de trabajo", "¿Qué se automatiza y con qué lógica?"),
    ("alba", "Implementación: Alba", "¿Cómo se conecta el marco con ETABS?"),
    ("resultados", "Resultados", "¿Qué muestran los tres modelos del caso?"),
    ("conclusiones", "Conclusiones", "¿Qué aporta el trabajo y qué queda abierto?"),
)
RAIL_LABELS = (
    "Problemática",
    "Objetivos",
    "Fundamentos",
    "Proceso manual",
    "Marco de trabajo",
    "Alba",
    "Resultados",
    "Conclusiones",
)

AGENDA_X = 1.9
AGENDA_TOP = 2.35
AGENDA_GAP = 0.66
RAIL_Y = -4.46
CAPTION_Y = -4.27


class SectionIndex:
    """Reutiliza una instancia por escena; ``build`` abre divisor y contenido."""

    def __init__(self, scene: Scene):
        self.scene = scene
        self._previous: int | None = None
        self._visits = 0
        self._fills: list[Drawable] = []
        self._captions: list[Text] = []

    def build(self, section: Section, *, transition: Transition | None = None) -> None:
        self.show(section.key, transition=transition or Transition.cross_fade(0.45))
        active = self._previous
        assert active is not None
        self.scene.play(self._fills[active].animate.fill_level(0), duration=0)
        section.build(self.scene, on_enter=self.advance)

    def show(self, key: str, *, transition: Transition | None = None) -> None:
        keys = [k for k, _, _ in SECTIONS]
        if key not in keys:
            raise ValueError(f"Bloque desconocido {key!r}; opciones: {', '.join(keys)}")
        active = keys.index(key)
        previous = self._previous
        scene = self.scene
        self._visits += 1
        _, title, question = SECTIONS[active]
        _ = scene.segment(
            f"Índice · {title}",
            transition,
            notes=(
                f"Bloque {active + 1} de {len(SECTIONS)}: {title}. "
                f"Pregunta guía: {question} Transición breve, 5-10 s."
            ),
        )
        _ = scene.camera.reset()

        if not self._fills:
            self._build_rail()

        # Odómetro manual: el numeral anterior sale hacia arriba y el nuevo entra desde abajo.
        window = (
            scene.geometry.rect(3.4, 1.55)
            .no_fill()
            .no_stroke()
            .move_to(LEFT_EDGE + 1.7, 2.02)
        )
        roll = 1.6
        numeral_new = t(
            scene,
            f"{active + 1:02d}",
            LEFT_EDGE,
            1.3 - (roll if previous is not None else 0),
            font=DISPLAY,
            size=1.55,
            weight=700,
            color=BRICK,
            anchor=Anchor.BOTTOM_LEFT,
        )
        numeral_new.clip(window)
        numeral_old = None
        if previous is not None:
            numeral_old = t(
                scene,
                f"{previous + 1:02d}",
                LEFT_EDGE,
                1.3,
                font=DISPLAY,
                size=1.55,
                weight=700,
                color=BRICK,
                anchor=Anchor.BOTTOM_LEFT,
            )
            numeral_old.clip(window)
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

        rows: list[Drawable] = []
        for i, (_, name, _) in enumerate(SECTIONS):
            y = AGENDA_TOP - i * AGENDA_GAP
            done = i < active
            color = BRICK if i == active else (INK_SOFT if done else MUTED)
            rows.append(
                t(
                    scene,
                    f"{i + 1:02d}",
                    AGENDA_X,
                    y,
                    font=MONO,
                    size=0.2,
                    color=color,
                    anchor=Anchor.LEFT,
                )
            )
            rows.append(
                t(
                    scene,
                    name,
                    AGENDA_X + 0.65,
                    y,
                    font=SANS,
                    size=0.3,
                    weight=900 if i == active else 400,
                    color=INK if i == active else color,
                    anchor=Anchor.LEFT,
                )
            )
        start = previous if previous is not None else active
        marker = (
            scene.geometry.rounded_rect(0.07, 0.42, 0.035)
            .fill(BRICK)
            .no_stroke()
            .move_to(AGENDA_X - 0.3, AGENDA_TOP - start * AGENDA_GAP)
        )

        numerals = [n for n in (numeral_old, numeral_new) if n is not None]
        scene.play(
            stagger(
                parallel(*[n.animate.fade_in().duration(0.4) for n in numerals]),
                heading.animate.fade_in_from(Direction.UP, 0.12).duration(0.6),
                prompt.animate.fade_in().duration(0.5),
                prompt_rule.animate.create().duration(0.5),
                divider.animate.create().duration(0.5),
                stagger(*[r.animate.fade_in().duration(0.3) for r in rows], each=0.02),
                marker.animate.fade_in().duration(0.3),
                each=0.08,
            )
        )
        animations = [
            marker.animate.move_to(
                AGENDA_X - 0.3, AGENDA_TOP - active * AGENDA_GAP
            ).duration(0.7),
        ]
        animations += [
            fill.animate.fill_level(1 if i < active else 0).duration(0.7)
            for i, fill in enumerate(self._fills)
        ]
        animations += [
            caption.animate.fill(BRICK if i == active else MUTED).duration(0.5)
            for i, caption in enumerate(self._captions)
        ]
        if numeral_old is not None:
            animations += [
                numeral_old.animate.shift_by(0, roll).duration(0.7),
                numeral_new.animate.shift_by(0, roll).duration(0.7).delay(0.02),
            ]
        scene.play(animations)
        scene.stop(f"entrada-{key}")
        self._previous = active

    def _build_rail(self) -> None:
        scene = self.scene
        n = len(SECTIONS)
        gap = 0.08
        width = (16 - 2 * 0.7 - gap * (n - 1)) / n
        visuals: list[Drawable] = []
        for i, name in enumerate(RAIL_LABELS):
            x = -8 + 0.7 + width / 2 + i * (width + gap)
            rail = (
                scene.geometry.rect(width, 0.04)
                .fill(FAINT)
                .no_stroke()
                .move_to(x, RAIL_Y)
                .hud()
                .z_index(100)
            )
            fill = (
                scene.geometry.fill_level(
                    rail, BRICK, 0, direction="left", keep_outline=False
                )
                .hud()
                .z_index(101)
            )
            caption = (
                t(
                    scene,
                    name.upper(),
                    x - width / 2,
                    CAPTION_Y,
                    font=SANS,
                    size=0.115,
                    weight=900,
                    color=MUTED,
                    anchor=Anchor.LEFT,
                )
                .hud()
                .z_index(101)
            )
            self._fills.append(fill)
            self._captions.append(caption)
            visuals += [rail, fill, caption]
        scene.persist(*visuals)
        scene.play([v.animate.fade_in() for v in visuals], duration=0.35)

    def advance(self, scene: Scene, progress: SectionProgress) -> None:
        """Al entrar a cada escena el tramo activo del riel avanza."""
        if self._previous is None:
            raise ValueError("show() debe llamarse antes de advance()")
        scene.play(
            self._fills[self._previous].animate.fill_level(progress.fraction),
            duration=0.35,
        )
