"""Captura de revisión: una imagen por pausa, sin depender de la GUI.

``gaanim --diff --example . --capture-only --no-gui`` define GAANIM_SNAPSHOTS.
En ese modo ``create_scene`` devuelve un ``TimedScene``: reenvía todo a la
escena real y acumula el cursor de la línea de tiempo para conocer el instante
de cada ``stop``. Fuera de ese modo la presentación usa la ``Scene`` nativa.
"""

import json
import os
from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Any

from gaanim import Composition, Easing, Scene, parallel

if TYPE_CHECKING:
    from gaanim.gaanim_core import Playable

SNAPSHOT_ENV = "GAANIM_SNAPSHOTS"


class TimedScene:
    """Proxy de ``Scene`` que registra el tiempo de cada pausa."""

    def __init__(self, scene: Scene) -> None:
        self._scene = scene
        self._cursor = 0.0
        self._segment = ""
        self.stops: list[tuple[float, str, str]] = []

    def __getattr__(self, name: str) -> Any:
        return getattr(self._scene, name)

    def play(
        self,
        items: "Playable | Sequence[Playable]",
        *,
        duration: float | None = None,
        easing: Easing | None = None,
    ) -> None:
        batch = list(items) if isinstance(items, Sequence) else [items]
        composition: Composition = parallel(*batch)
        span = composition.schedule(duration=duration).span
        self._scene.play(items, duration=duration, easing=easing)
        self._cursor += span

    def wait(self, seconds: float) -> None:
        self._scene.wait(seconds)
        self._cursor += seconds

    def stop(self, name: str | None = None) -> None:
        self._scene.stop(name)
        self.stops.append((self._cursor, self._segment, name or ""))

    def segment(self, name: str, *args: Any, **kwargs: Any) -> Any:
        self._segment = name
        return self._scene.segment(name, *args, **kwargs)

    def capture(self) -> None:
        """Pide una imagen justo antes de cada pausa y guarda el índice."""
        directory = os.environ[SNAPSHOT_ENV]
        # Un instante antes de la pausa evita capturar el inicio del siguiente segmento.
        times = [max(0.0, time - 0.02) for time, _, _ in self.stops]
        only = os.environ.get("TESIS_ONLY")
        if only:
            chosen = {int(index) for index in only.split(",")}
            times = [time for index, time in enumerate(times) if index in chosen]
        index = [
            {"stop": i, "time": round(t, 3), "segment": s, "name": n}
            for i, (t, s, n) in enumerate(self.stops)
        ]
        Path(directory).mkdir(parents=True, exist_ok=True)
        (Path(directory) / "stops.json").write_text(
            json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8"
        )
        self._scene.snapshots(directory, times)


def wrap(scene: Scene) -> Scene:
    if os.environ.get(SNAPSHOT_ENV):
        return TimedScene(scene)  # pyright: ignore[reportReturnType]
    return scene


def finish(scene: Scene) -> None:
    if isinstance(scene, TimedScene):
        scene.capture()
    scene.render()
