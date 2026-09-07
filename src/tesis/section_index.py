from gaanim import (
    BLACK,
    Color,
    Direction,
    Scene,
    TextAnchor,
    Transition,
    parallel,
    stagger,
)

from tesis.theme import ACCENT

SECTIONS = (
    ("problematica", "Problemática"),
    ("objetivos", "Objetivos"),
    ("fundamentos", "Fundamentos"),
    ("propuesta", "Propuesta"),
    ("resultados", "Resultados"),
    ("conclusiones", "Conclusiones"),
)

MUTED = Color.from_hex("#C7C8CD")
SECONDARY = Color.from_hex("#888B95")
LABEL_X = -5
NUMBER_X = -6.2
FIRST_Y = 0
ROW_GAP = 1.5


class SectionIndex:
    """Keep the previous selection and animate it into each new section.

    Reuse one instance throughout a Scene. Each show() creates a segment and
    a named stop. The global rail persists across content segments and camera moves.
    """

    def __init__(self, scene: Scene):
        self.scene: Scene = scene
        self._previous: int | None = None
        self._visits: int = 0
        self._rail_fills = []
        self._rail_labels = []

    def show(self, key: str, *, transition: Transition | None = None) -> None:
        keys = [section_key for section_key, _ in SECTIONS]
        if key not in keys:
            raise ValueError(f"Unknown section {key!r}; choose from {', '.join(keys)}")
        active = keys.index(key)
        previous = self._previous
        origin = previous if previous is not None else active
        scene = self.scene
        self._visits += 1
        _ = scene.segment(
            f"Índice · {SECTIONS[active][1]} · {self._visits}",
            transition,
            notes=f"Entrada al bloque {active + 1} de {len(SECTIONS)}: {SECTIONS[active][1]}.",
        )
        _ = scene.camera.reset()

        def text(content: str, x: float, y: float, *, size: float = 1, color: Color=MUTED):
            return scene.text(content, size=size).fill(color).move_to(x, y, TextAnchor.BASELINE_LEFT)

        labels = [
            text(
                f"*{label}*",
                LABEL_X + (0.14 if i == previous else 0),
                FIRST_Y - (i - origin) * ROW_GAP,
                color=BLACK if i == previous else MUTED,
            )
            for i, (_, label) in enumerate(SECTIONS)
        ]
        number = scene.viz.rolling_number(
            previous + 1 if previous is not None else 0,
            decimals=0,
            min_digits=2,
            font_size=1.1,
            mode="odometer",
            direction="up",
            color=ACCENT,
        ).move_to(NUMBER_X, FIRST_Y, TextAnchor.BASELINE_LEFT)

        if not self._rail_fills:
            width = (16 - 0.1 * (len(SECTIONS) - 1)) / len(SECTIONS)
            footer = (scene.geometry.rect(16, 0.4).fill("#F0F1F4")
                      .no_stroke().move_to(0, -4.3).hud().z_index(98))
            separator = (scene.geometry.line(-8, -4.1, 8, -4.1)
                         .stroke("#DDE0E6", 0.012).hud().z_index(99))
            visuals = [footer, separator]
            for i, (_, label) in enumerate(SECTIONS):
                x = -8 + width / 2 + i * (width + 0.1)
                rail = (scene.geometry.rect(width, 0.05).fill("#DDE0E6")
                        .no_stroke().move_to(x, -4.475).hud().z_index(100))
                fill = scene.geometry.fill_level(
                    rail, ACCENT, 0, direction="left", keep_outline=False,
                ).hud().z_index(101)
                caption = (scene.text(f"*{label}*", size=0.16).fill(SECONDARY)
                           .move_to(x, -4.34, TextAnchor.BASELINE_CENTER)
                           .hud().z_index(101))
                self._rail_fills.append(fill)
                self._rail_labels.append(caption)
                visuals.extend([rail, fill, caption])
            scene.persist(*visuals)
            scene.play([item.animate.fade_in() for item in visuals], duration=0.35)
        if previous is None:
            scene.play(
                parallel(
                    number.visual.animate.fade_in(),
                stagger(
                    *[
                        label.animate.fade_in_from(
                            Direction.DOWN, distance=0.1
                        ).duration(0.4)
                        for label in labels
                    ],
                    each=0.045,
                ))
            )
        else:
            visible = [*labels, number.visual]
            scene.play([item.animate.fade_in() for item in visible], duration=1)

        if previous != active:
            current_title = text(
                f"*{SECTIONS[active][1]}*",
                LABEL_X + 0.14,
                FIRST_Y,
                color=BLACK,
            )
            animations = [
                labels[active].animate.transform_to(current_title),
                number.count_to(active + 1, duration=1),
            ]
            animations.extend(
                fill.animate.fill_level(1 if i < active else 0)
                for i, fill in enumerate(self._rail_fills)
            )
            animations.extend(
                label.animate.fill(ACCENT if i == active else SECONDARY)
                for i, label in enumerate(self._rail_labels)
            )
            for i, label in enumerate(labels):
                if i not in (active, previous):
                    animations.append(label.animate.shift_by(0, (active - origin) * ROW_GAP))
            if previous is not None:
                previous_label = text(
                    f"*{SECTIONS[previous][1]}*", LABEL_X, FIRST_Y - (previous - active) * ROW_GAP
                )
                animations += [
                    labels[previous].animate.transform_to(previous_label),
                ]
            scene.play(animations, duration=1)
        else:
            scene.wait(1)
        scene.stop(f"entrada-{key}-{self._visits}")
        self._previous = active

    def advance(self, segment: int, total: int) -> None:
        """Advance the current section by its content-segment ordinal (1-based)."""
        if self._previous is None:
            raise ValueError("Call show() before advancing a section")
        if total < 1 or not 1 <= segment <= total:
            raise ValueError("Expected 1 <= segment <= total")
        self.scene.play(
            self._rail_fills[self._previous].animate.fill_level(segment / total),
            duration=0.35,
        )
