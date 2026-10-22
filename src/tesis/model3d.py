"""Mundo 3D de los modelos de ETABS: coordenadas, tomas de cámara y rótulos de pantalla.

Los modelos se escriben en metros, como en ETABS: x a lo largo de la fachada (ejes
1–7), y en profundidad (ejes A–D) y z hacia arriba. Gaanim usa y hacia arriba y z
hacia el espectador, así que ``world`` lleva (x, y, z) a (x, z, −y): la fachada del
eje A mira a la cámara.

Una toma (``Shot``) encuadra el modelo con una cámara en perspectiva que mira a un
foco: dice desde dónde se mira (azimut y elevación), cuánto mide un metro del plano del
foco en la pantalla y en qué punto de la pantalla queda el foco: así el modelo se ve a
la izquierda, junto al panel de pasos, en cualquier toma. ``orbit_to`` pasa de una toma
a otra rodeando el foco en lugar de cruzar el modelo en línea recta. Con la cámara en
perspectiva la capa 2D no se mueve: encabezado, paneles y fuentes quedan en su sitio.
Cada diapositiva empieza en la vista 2D (``camera="reset"`` en ``section_index``).
"""

import math
from dataclasses import dataclass, replace

from gaanim import Anchor, Anim, CameraState, Drawable, Easing, EasingCurve, Scene

type P2 = tuple[float, float]
type P3 = tuple[float, float, float]

LENS = 0.42  # rad: campo de visión vertical, una perspectiva suave (≈ 24°)
GLIDE = Easing.ease_in_out(EasingCurve.CUBIC)


def world(x: float, y: float, z: float) -> P3:
    """Punto del modelo (m, z hacia arriba) en el mundo de Gaanim (y hacia arriba)."""
    return x, z, -y


@dataclass(frozen=True)
class Shot:
    """Toma de la cámara: dirección de la mirada, escala del foco y dónde se ve."""

    azimuth: float  # grados, desde la fachada A (mirando hacia +y) hacia +x
    elevation: float  # grados sobre el horizonte; hasta 90, en planta
    scale: float  # unidades de escena por metro en el plano del foco
    focus: P3  # punto del modelo, m
    at: P2  # dónde queda el foco en la pantalla, en unidades de escena

    def turned(self, azimuth: float, elevation: float | None = None) -> "Shot":
        return replace(
            self,
            azimuth=azimuth,
            elevation=self.elevation if elevation is None else elevation,
        )

    def state(self, scene: Scene) -> CameraState:
        """La pose de la toma: una órbita en perspectiva alrededor del foco.

        El azimut de Gaanim parte del lado +z del mundo, que es la fachada A.
        """
        return scene.camera.state_orbit(
            world(*self.focus),
            math.radians(self.azimuth),
            math.radians(self.elevation),
            scale=self.scale,
            fov_y=LENS,
            screen_offset=self.at,
        )

    def project(self, scene: Scene, point: P3) -> P2:
        """Dónde dibuja la toma un punto del modelo, en unidades de la pantalla."""
        return scene.camera.project(world(*point), self.state(scene))


def orbit_to(
    scene: Scene, shot: Shot, duration: float = 1.4, easing: Easing = GLIDE
) -> Anim:
    """Lleva la cámara a ``shot`` rodeando el foco: gira, sube y se acerca a la vez.

    El foco no sale de su lugar en la pantalla mientras la toma cambia de lado.
    """
    return (
        scene.camera.animate.to(shot.state(scene), path="orbit")
        .duration(duration)
        .easing(easing)
    )


def anchor(scene: Scene, point: P3) -> Drawable:
    """Punto invisible del modelo: extremo de frames y ancla de rótulos que se mueven."""
    return scene.geometry.dot(0.001).no_fill().no_stroke().move_to_3d(*world(*point))


def lay_flat(drawable: Drawable, z: float = 0.0) -> Drawable:
    """Tiende en el nivel ``z`` un objeto 2D dibujado en planta (x, y en metros).

    El objeto debe agruparse con ``origin=(0, 0)``: así el origen de la planta cae
    en el origen del modelo y sus coordenadas son las de ETABS.
    """
    return drawable.in_3d().rotate_to_3d(-math.pi / 2, 0, 0).move_to_3d(*world(0, 0, z))


def pinned(
    drawable: Drawable,
    at: P3,
    offset: P2 = (0.0, 0.0),
    anchor: Anchor | None = None,
) -> Drawable:
    """Rótulo 2D sobre un punto del modelo, de frente a la cámara y de tamaño fijo.

    Un billboard oculto que el pase 3D dibuja donde la cámara ve el punto, gire o se
    acerque, sin un updater por fotograma. ``anchor`` es el punto de su caja que cae
    sobre el punto (su origen si se omite) y ``offset`` lo corre en unidades de
    pantalla. Se mueve con ``move_to_3d``.
    """
    return (
        drawable.move_to_3d(*world(*at))
        .billboard(offset=offset, anchor=anchor)
        .hidden()
    )
