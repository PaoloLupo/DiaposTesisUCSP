"""Mundo 3D de los modelos de ETABS: coordenadas, cámara y rótulos de pantalla.

Los modelos se escriben en metros, como en ETABS: x a lo largo de la fachada (ejes
1–7), y en profundidad (ejes A–D) y z hacia arriba. Gaanim usa y hacia arriba y z
hacia el espectador, así que ``world`` lleva (x, y, z) a (x, z, −y): la fachada del
eje A mira a la cámara.

``CameraRig`` encuadra el modelo con una cámara en perspectiva que gira alrededor de un
foco. Una toma (``Shot``) dice desde dónde se mira (azimut y elevación), cuánto mide un
metro del plano del foco en la pantalla y en qué punto de la pantalla queda el foco: así
el modelo se ve a la izquierda, junto al panel de pasos, en cualquier toma. Pasar de una
toma a otra es animar esos parámetros, de modo que la cámara viaja por una esfera
alrededor del foco en lugar de cruzar el modelo en línea recta. Con la cámara en
perspectiva la capa 2D no se mueve: encabezado, paneles y fuentes quedan en su sitio.
"""

import math
from dataclasses import dataclass, replace

from gaanim import (
    Anim,
    CameraConstraint,
    CameraState,
    Drawable,
    Easing,
    EasingCurve,
    Parameter,
    Scene,
    computed,
)

type P2 = tuple[float, float]
type P3 = tuple[float, float, float]

FRAME_HEIGHT = 9.0  # alto del cuadro, en unidades de escena
LENS = 0.42  # rad: campo de visión vertical, una perspectiva suave (≈ 24°)
GLIDE = Easing.ease_in_out(EasingCurve.CUBIC)

# Restricciones de cámara activas: se sueltan al entrar a la siguiente diapositiva.
_ACTIVE: list[CameraConstraint] = []


def world(x: float, y: float, z: float) -> P3:
    """Punto del modelo (m, z hacia arriba) en el mundo de Gaanim (y hacia arriba)."""
    return x, z, -y


def release_camera(scene: Scene) -> None:
    """Suelta los rigs 3D activos y devuelve la cámara a la vista 2D de las diapositivas."""
    if not _ACTIVE:
        return
    for constraint in _ACTIVE:
        constraint.disable()
    _ACTIVE.clear()
    scene.camera.reset()


@dataclass(frozen=True)
class Shot:
    """Toma de la cámara: dirección de la mirada, escala del foco y dónde se ve."""

    azimuth: float  # grados, desde la fachada A (mirando hacia +y) hacia +x
    elevation: float  # grados sobre el horizonte; menos de 90
    scale: float  # unidades de escena por metro en el plano del foco
    focus: P3  # punto del modelo, m
    at: P2  # dónde queda el foco en la pantalla, en unidades de escena

    def turned(self, azimuth: float, elevation: float | None = None) -> "Shot":
        return replace(
            self,
            azimuth=azimuth,
            elevation=self.elevation if elevation is None else elevation,
        )


def _pose(
    azimuth: float,
    elevation: float,
    scale: float,
    focus: P3,
    at: P2,
    lens: float = LENS,
) -> tuple[P3, P3]:
    """Ojo y objetivo (mundo) de una toma; ángulos en radianes."""
    ca, sa = math.cos(azimuth), math.sin(azimuth)
    ce, se = math.cos(elevation), math.sin(elevation)
    toward_eye = (sa * ce, -ca * ce, se)  # del foco al ojo, en el modelo
    right = (ca, sa, 0.0)
    up = (-se * sa, se * ca, ce)
    distance = FRAME_HEIGHT / (2 * scale * math.tan(lens / 2))
    sx, sy = at
    target = tuple(
        f - (sx / scale) * r - (sy / scale) * u
        for f, r, u in zip(focus, right, up, strict=True)
    )
    eye = tuple(t + distance * d for t, d in zip(target, toward_eye, strict=True))
    return world(*eye), world(*target)


class CameraRig:
    """Cámara en perspectiva que sigue una toma; ``to`` la lleva a otra.

    Los parámetros (azimut, elevación, logaritmo de la escala, foco y punto de
    pantalla) mueven dos puntos invisibles, el ojo y el objetivo, a los que se ata
    la cámara con ``bind_3d``. Animarlos con la misma curva hace que la cámara gire,
    se acerque y se desplace a la vez, sin que el foco salga de cuadro.
    """

    def __init__(self, scene: Scene, shot: Shot, *, lens: float = LENS) -> None:
        self.scene = scene
        self.lens = lens
        self.shot = shot
        viz = scene.viz
        self.azimuth = viz.parameter(math.radians(shot.azimuth))
        self.elevation = viz.parameter(math.radians(shot.elevation))
        self.log_scale = viz.parameter(math.log(shot.scale))
        self.focus = [viz.parameter(v) for v in shot.focus]
        self.at = [viz.parameter(v) for v in shot.at]
        inputs: list[Parameter] = [
            self.azimuth,
            self.elevation,
            self.log_scale,
            *self.focus,
            *self.at,
        ]

        def pose(a: float, e: float, ls: float, *rest: float) -> tuple[P3, P3]:
            fx, fy, fz, sx, sy = rest
            return _pose(a, e, math.exp(ls), (fx, fy, fz), (sx, sy), lens)

        def coordinate(which: int, axis: int):  # noqa: ANN202 - Computed
            return computed(lambda *values: pose(*values)[which][axis], inputs=inputs)

        def point(which: int) -> Drawable:
            return (
                scene.geometry.dot(0.001)
                .no_fill()
                .no_stroke()
                .move_to_3d(*(coordinate(which, axis) for axis in range(3)))
            )

        self._eye = point(0)
        self._target = point(1)
        self._constraint = scene.camera.bind_3d(
            eye=self._eye, target=self._target, fov_y=lens
        )
        _ACTIVE.append(self._constraint)

    def to(
        self, shot: Shot, duration: float = 1.4, easing: Easing = GLIDE
    ) -> list[Anim]:
        """Animaciones que llevan la cámara de la toma actual a ``shot``."""

        def move(parameter: Parameter, value: float) -> Anim:
            return parameter.animate.set(value).duration(duration).easing(easing)

        anims = [
            move(self.azimuth, math.radians(shot.azimuth)),
            move(self.elevation, math.radians(shot.elevation)),
            move(self.log_scale, math.log(shot.scale)),
        ]
        old = self.shot
        anims += [
            move(p, v)
            for p, v, before in zip(self.focus, shot.focus, old.focus, strict=True)
            if v != before
        ]
        anims += [
            move(p, v)
            for p, v, before in zip(self.at, shot.at, old.at, strict=True)
            if v != before
        ]
        self.shot = shot
        return anims

    def state(self, shot: Shot | None = None) -> CameraState:
        """La pose de ``shot`` (la toma actual si se omite), para proyectar puntos."""
        s = shot or self.shot
        eye, target = _pose(
            math.radians(s.azimuth),
            math.radians(s.elevation),
            s.scale,
            s.focus,
            s.at,
            self.lens,
        )
        return self.scene.camera.state_3d(eye=eye, target=target, fov_y=self.lens)

    def project(self, point: P3, shot: Shot | None = None) -> P2:
        """Dónde dibuja la toma un punto del modelo, en unidades de la pantalla."""
        return self.scene.camera.project(world(*point), self.state(shot))


def anchor(scene: Scene, point: P3) -> Drawable:
    """Punto invisible del modelo: extremo de frames y ancla de rótulos que se mueven."""
    return scene.geometry.dot(0.001).no_fill().no_stroke().move_to_3d(*world(*point))


def beneath(drawable: Drawable) -> Drawable:
    """Marca un objeto del pase 3D, que se dibuja debajo de toda la capa 2D.

    ``gaanim check`` compara las coordenadas propias de los objetos ``in_3d`` y de
    los billboards (metros, o el origen del rótulo) con las de los textos de la
    pantalla; sin esta marca avisaría de textos ocultos que no lo están.
    """
    return drawable.covers_on_purpose()


def lay_flat(drawable: Drawable, z: float = 0.0) -> Drawable:
    """Tiende en el nivel ``z`` un objeto 2D dibujado en planta (x, y en metros).

    El objeto debe agruparse con ``origin=(0, 0)``: así el origen de la planta cae
    en el origen del modelo y sus coordenadas son las de ETABS.
    """
    drawable.in_3d().rotate_to_3d(-math.pi / 2, 0, 0).move_to_3d(*world(0, 0, z))
    return beneath(drawable)


def pinned(
    scene: Scene,
    drawable: Drawable,
    at: P3,
    offset: P2 = (0.0, 0.0),
) -> Drawable:
    """Rótulo 2D sobre un punto del modelo, de frente a la cámara y de tamaño fijo.

    Devuelve un grupo oculto con el rótulo corrido ``offset`` (unidades de pantalla)
    desde el punto: un billboard que el pase 3D dibuja donde la cámara ve el punto,
    gire o se acerque, sin un updater por fotograma. Se mueve con ``move_to_3d``.
    """
    drawable.shift_by(*offset)
    group = scene.geometry.group([drawable], origin=(0, 0))
    return beneath(group.move_to_3d(*world(*at)).billboard().hidden())
