# Notas para Gaanim

Hallazgos al preparar las diapositivas de tesis con Gaanim 0.4.2 (build del 26-09-2026 con
cámaras secundarias), Windows 11. Cada entrada dice cómo reproducirla, qué se esperaba y el
rodeo usado en este proyecto. Solo se anota lo comprobado renderizando fotogramas.

## Estado en 0.5.2 (27-09-2026)

Todo lo anotado aquí quedó resuelto en 0.5.0 (bugs 1–4 y las cinco mejoras: `scene.stop(...,
loop=)`, `drawable.bounds()`, `inset(aspect=/size=)`, `imagen.pixel(px, py)` y
`matrix_to`). Los rodeos de los bugs 2 y 3 se quitaron del proyecto; el `with_pivot` del
anillo del contador se mantiene porque gira sobre el centro del arco, no el de su caja.
`scene.text.measure` ya no existe: se migró a `bounds()`, lo que abrió el bug 5 (abierto).

## Bugs y comportamientos inesperados

### 1. El pivote por defecto de la geometría absoluta es el origen de la escena
- **Reproducir:** `arc = scene.geometry.curved_arrow_arc(0, -2.5, 0.38, 1.9, 5.2)` y
  `scene.play(arc.animate.rotate_by(2 * math.pi))`.
- **Obtenido:** el arco orbita alrededor de `(0, 0)` en vez de girar sobre sí mismo. Pasa con
  toda figura declarada con coordenadas absolutas (`line(x0, y0, x1, y1)`, `polygon([...])`,
  `curved_arrow_arc(cx, cy, ...)`): su pivote queda en el origen.
- **Estado:** `grow_from_center()` ya se corrigió (crece desde el centro de la caja), pero
  `rotate_by`, `rotate_to`, `scale_to` y `skew_to` siguen usando el origen.
- **Esperado:** el mismo criterio que `grow_from_center`: pivote en el centro de la caja
  cuando no hay `with_pivot`, o al menos documentar cuál es el pivote por defecto (la
  referencia de `rotate_to` dice «alrededor del pivote» sin decir cuál es).
- **Rodeo:** `.with_pivot(cx, cy)` explícito (anillo del contador en *traslado manual*).

### 2. `CameraView.animate.pop_in()` deja la pantalla encogida y visible
- **Reproducir:** un `scene.camera.inset(..., layers=["rayos-x"])` con objetos en esa capa;
  `pop_out()` y luego `pop_in()`.
- **Obtenido:** tras `pop_in` la pantalla queda sobre la región, a tamaño real, y sigue
  mostrando la vista; con una capa de vista revela su contenido encima de la escena.
- **Esperado:** que `pop_in` termine con la pantalla oculta (es la salida simétrica de
  `pop_out`, que sí hace de entrada), o un parámetro para ocultarla.
- **Rodeo:** `sequence(view.animate.pop_in(), parallel(fade_out de view.screen, view.frame y
  view.connectors))`.

### 3. `mechanics.dimension_between` no se dibuja sin animación de entrada
- **Reproducir:** `scene.mechanics.dimension_between((-5.5, 0.1), (-2.5, 0.1), 0.3,
  side="above", label="control")` sin animarla, y `scene.render()`.
- **Obtenido:** la cota no aparece en ningún fotograma. Con
  `scene.play(dim.animate.fade_in())` sí se ve.
- **Esperado:** la regla general de la documentación: un objeto sin animación de entrada es
  visible desde su declaración (así se comportan `rect`, `text`, `line`…).
- **Rodeo:** darle siempre una entrada (`fade_in`), también a las cotas que viven en una capa
  de vista (cotas del inset de densidad).

### 4. La nota de migración de los SVG (0.4.1) sobre los trazos se presta a confusión
- **Texto:** «Los anchos fijados con `.stroke(color, ancho)` no cambian».
- **Obtenido:** el ancho de `.stroke()` se escala con `scale_to`. Un SVG que compensaba la
  escala antigua con `scale_to(0.0058)` y `stroke(c, 1.6)` pasa a `scale_to(0.58)`, y su trazo
  mide ahora ~0.93 unidades: hay que dividirlo también entre 100.
- **Sugerencia:** decir explícitamente que, si el SVG se escala con `scale_to`, el ancho
  fijado con `.stroke()` también debe dividirse entre 100.

### 5. `drawable.bounds()` cuesta ~0.5 s por llamada en una escena grande (0.5.2, abierto)
- **Reproducir:** sustituir los `scene.text.measure(...)` retirados en 0.5.0 por
  `texto.bounds().width` (tal como indica la nota de migración) en esta presentación
  (41 segmentos, 78 pausas, 274 s). Son 54 llamadas: filas de pastillas, el tramo de cada
  valor copiado que luego se tacha en *traslado manual*, anchos de encabezados.
- **Obtenido:** `gaanim .` pasa de ~2 s a 19 s de Python (`Python 18.54s · replay 0.48s`).
  Cronometrando cada llamada: 300–600 ms, que crecen con la escena escrita hasta ese punto;
  las 54 suman 16.6 s. El docstring lo anticipa («Each call compiles the scene authored so
  far»), pero con la medida de texto retirada no queda alternativa barata y el coste es
  cuadrático al medir dentro de un bucle.
- **Esperado:** medir un texto o una figura sin animaciones no debería compilar la escena
  entera: su caja depende solo de su contenido, estilo y transformaciones. Algo como
  compilar solo el subárbol del objeto (y sus animaciones terminadas antes del cursor), o
  cachear la compilación entre llamadas consecutivas sin cambios intermedios. La nota de
  migración debería avisar del coste, o conservar `scene.text.measure` como vía rápida.
- **Rodeos posibles (no aplicados aún):** `next_to` para las filas de pastillas (se resuelve
  al compilar, sin medir); medir los textos en una escena auxiliar vacía con el mismo tema
  y cachear por (contenido, estilo, tamaño, peso, fuente).

## Mejoras sugeridas

- **Animaciones durante una pausa:** `scene.stop()` congela la imagen, así que un movimiento
  continuo (las flechas de la placa de Nazca) solo puede mostrarse antes de la pausa. Sería
  útil un bucle ambiental que siga mientras el orador habla, por ejemplo
  `scene.stop("dos-placas", loop=anim)` o animaciones marcadas como ambientales.
- **Medidas de un objeto ya creado:** no hay `bounds()`/`width` en `Drawable` ni en `Text`.
  Para tachar un valor hay que repetir su contenido y estilo en `scene.text.measure(...)`.
  Un `drawable.bounds()` (en unidades de escena) evitaría duplicar el texto.
- **Proporción del inset rectangular:** `scene.camera.inset(..., shape="rect")` toma siempre la
  proporción del fotograma (16:9). Para ampliar una barra de herramientas o un panel alto hay
  que recortar el detalle; un parámetro `aspect=` (o `size=(w, h)`) dejaría encuadrarlo entero.
- **Píxeles de una imagen a coordenadas de escena:** para señalar zonas de una captura hay que
  convertir a mano `x_izq + px · escala`. Es fácil equivocarse al medir sobre una captura ya
  reducida (pasó con la interfaz de Alba). Un `image.point(px, py)` que devuelva el
  `AnchorPoint` de un píxel de la imagen, usable en `move_to`, `inset` o `pan_to`, lo evitaría.
- **Transformación afín general:** `skew_to` sesga en pantalla, lo que sirve para alzados pero
  no para un corte en isométrica (la altura en pantalla mezcla cota y profundidad). Un setter
  afín 2D (`transform_to(matrix)`) o un sesgo a lo largo de ejes arbitrarios permitiría
  deformar caras en isométrica sin trocearlas.
