from gaanim import (
    BLACK,
    RED,
    Anchor,
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
    a named stop; the following content segment automatically removes it.
    """

    def __init__(self, scene: Scene):
        self.scene: Scene = scene
        self._previous: int | None = None
        self._visits: int = 0

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

        rail = (
            scene.geometry.rect(18, 0.1).fill("#DDE0E6").no_stroke().move_to(0, 4.5, Anchor.TOP)
        )
        progress = scene.geometry.fill_level(
            rail,
            ACCENT,
            (previous + 1) / len(SECTIONS) if previous is not None else 0,
            direction="left",
            keep_outline=False,
        ).glow(ACCENT, 0.05)
        scene.play([rail.animate.fade_in()], duration=0.35)
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
                progress.animate.fill_level((active + 1) / len(SECTIONS)),
                number.count_to(active + 1, duration=1),
            ]
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
