"""Mundo 3D de los modelos de ETABS: tomas de cámara y rótulos de pantalla.

Los modelos se escriben en metros, como en ETABS: x a lo largo de la fachada (ejes
1–7), y en profundidad (ejes A–D) y z hacia arriba. La escena tiene z hacia arriba
(``Scene(up="z")`` en ``tesis.app``), así que esas coordenadas son las del mundo: la
fachada del eje A mira a la cámara.

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

from gaanim import (
    Anchor,
    Anim,
    CameraState,
    Drawable,
    Easing,
    EasingCurve,
    Parameter,
    Scene,
)

type P2 = tuple[float, float]
type P3 = tuple[float, float, float]

LENS = 0.42  # rad: campo de visión vertical, una perspectiva suave (≈ 24°)
GLIDE = Easing.ease_in_out(EasingCurve.CUBIC)


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

        Con z hacia arriba, el azimut de Gaanim parte del lado −y, que es la fachada A.
        """
        return scene.camera.state_orbit(
            self.focus,
            math.radians(self.azimuth),
            math.radians(self.elevation),
            scale=self.scale,
            fov_y=LENS,
            screen_offset=self.at,
        )

    def project(self, scene: Scene, point: P3) -> P2:
        """Dónde dibuja la toma un punto del modelo, en unidades de la pantalla."""
        return scene.camera.project(point, self.state(scene))


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
    return scene.geometry.dot(0.001).no_fill().no_stroke().move_to_3d(*point)


def carry(drawable: Drawable, offset: P3, amount: Parameter) -> Drawable:
    """Traslada ``drawable`` ``offset`` veces ``amount`` desde el cursor, sin deformarlo.

    Es ``deform`` con un campo igual en todo punto, que se suma a los movimientos
    propios del objeto. Ese campo no depende de la rejilla: se le da una región para
    que ``deform`` no mida el objeto.
    """
    return drawable.deform(
        lambda x, y, z: offset, amount=amount, samples=2, region=((0, 0, 0), (1, 1, 1))
    )


def lay_flat(drawable: Drawable, z: float = 0.0) -> Drawable:
    """Tiende en el nivel ``z`` un objeto 2D dibujado en planta (x, y en metros).

    Su pivote queda en el origen de la planta: con ``origin=(0, 0)`` en el grupo,
    ``move_to_3d(0, 0, z)`` lo lleva a otro nivel.
    """
    return drawable.in_3d(plane="xy", origin=(0.0, 0.0, z))


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
    return drawable.move_to_3d(*at).billboard(offset=offset, anchor=anchor).hidden()
