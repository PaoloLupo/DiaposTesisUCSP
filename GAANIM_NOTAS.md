# Notas para el repo principal de Gaanim

Hallazgos durante el rediseño de las diapositivas de tesis (Gaanim 0.2.0, Windows 11).
Cada entrada indica cómo reproducirla y el rodeo usado en este proyecto.

## Bugs

### 1. `gaanim --diff --example .` no acepta el directorio actual
- **Reproducir:** dentro de un proyecto, `gaanim --diff --example . --capture-only --no-gui`.
- **Obtenido:** `gaanim --diff: example has no file stem: .`
- **Esperado:** resolver `.` como el proyecto, igual que `gaanim .` y `gaanim check .`.
- **Rodeo:** ejecutar desde el directorio padre: `gaanim --diff --example DiaposTesisUCSP ...`.

### 2. Puntas de flecha desproporcionadas en `mechanics.dimension_between`
- **Reproducir:** `scene.mechanics.dimension_between((0, 0), (6, 0), -0.55, label="16.60 m", font_size=0.15, line_width=0.008)`.
- **Obtenido:** las puntas triangulares salen enormes (≈2 unidades de alto) y tapan el dibujo;
  no escalan con `line_width` ni con `font_size`, y no hay parámetro para su tamaño.
- **Esperado:** puntas proporcionales a la línea o un parámetro `head_size`.
- **Rodeo:** cota propia con líneas y marcas a 45° (`tesis.kit.dimension`).

### 3. `geometry.curved_arrow(...).stroke(...).no_fill()` dibuja trazos fuera de cuadro
- **Reproducir:** `scene.geometry.curved_arrow(4.4, -0.75, -5.15, -0.75, -0.35).stroke(color, 0.028).no_fill()`.
- **Obtenido:** varias líneas rectas largas que cruzan toda la escena en lugar de un arco.
- **Pendiente:** confirmar si `angle` espera grados o si el contorno de la flecha rellena
  no admite `no_fill()`; la docstring no indica unidades.
- **Rodeo:** `geometry.connector(start, end, via=[...])`.

### 4. `rolling_number(font_family=...)` no resuelve las fuentes de `Theme(font_files=...)` igual que `Text`
- **Reproducir:** registrar `Aleo-VariableFont.ttf` y los TTF estáticos de Lato con
  `Theme("paper", font_files={...})`; crear `scene.text("0123", font="Aleo")` y
  `scene.viz.rolling_number(1234.5, decimals=1, font_family="Aleo")`.
- **Obtenido:** el `Text` usa Aleo, pero el contador cae a otra fuente sans ligera.
  Con `font_family="Lato"` (o `None`) el contador usa la primera cara registrada de la familia
  (Lato Black, por orden alfabético del diccionario) y no hay parámetro de peso.
- **Esperado:** la misma resolución de familia y peso que `Text` (incluidas fuentes variables),
  o un parámetro `weight`.
- **Rodeo:** numerales de los divisores como `Text` con recorte y desplazamiento (odómetro manual);
  el diccionario de `font_files` se ordena para que Lato Bold sea la primera cara.

### 5. La marca `_` de `scene.text` rompe contenido técnico
- `scene.text("Valores: V_e del piso 1 (tb:agriet_xy)")` interpreta `_..._` como cursiva y, si
  queda un `_` impar, lanza `ValueError: unbalanced '_' text markup delimiter`. Es el comportamiento
  documentado, pero en contenido técnico (subíndices, etiquetas como `tb:dist_comp`, `X1_2`) es
  una trampa frecuente. Sugerencia: un parámetro `markup=False` en `scene.text`.
- **Rodeo:** `tesis.kit.plain()` escapa `_` fuera de `$...$`.

### 6. `CoordinateSpace.animate.view_to` deforma los marcadores de `scatter_data`
- **Reproducir:** `plane = scene.viz.cartesian_2d(Axis.linear(0, 0.55), Axis.linear(0.5, 4.5), width=5.6, height=3.5)`;
  `dots = plane.scatter_data(xs, ys, radius=0.055)`; luego
  `scene.play(plane.animate.view_to((0, 0.2), (0.5, 4.5)))`.
- **Obtenido:** los puntos se estiran como elipses horizontales (la escala del eje X cambia y
  el marcador escala con ella).
- **Esperado:** marcadores que conservan su radio en unidades de escena, como las líneas que
  conservan su grosor.
- **Rodeo:** segundo juego de ejes para el detalle, con transición de opacidad.

### 7. `z_index` sobre un `geometry.group` no parece reordenar el grupo
- **Observado:** `scene.geometry.group([box, text]).z_index(5)` quedó debajo de un círculo con
  `z_index(2)`, y un grupo `pill(...)` con `z_index(8)` quedó oculto bajo un rectángulo con
  `z_index(1)` creado antes. Con `z_index` en los hijos (caja 5, texto 6) el texto desapareció.
- **Pendiente:** confirmar con un ejemplo mínimo; puede que el orden solo aplique a hojas.
- **Rodeo:** reubicar los elementos para que no se superpongan.

## Mejoras sugeridas

- **Instantes de los `stop`:** no hay forma de consultar el cursor de la línea de tiempo desde
  Python (`Scene` no es subclasificable y sus atributos son de solo lectura), así que no se
  pueden pedir snapshots por pausa. `gaanim check` ya cuenta las pausas; exponer sus tiempos
  (p. ej. `gaanim --diff --capture-stops` o `scene.cursor`) facilitaría revisar presentaciones.
  Rodeo: proxy `tesis.review.TimedScene` que suma `Composition.schedule().span`.
- **`rolling_number(mode="continuous")`:** al terminar `count_to`, las ruedas altas pueden quedar
  entre dígitos (documentado), lo que deja cifras ilegibles como «6?.8 %». Sería útil que el
  modo continuo se asiente en el valor final al terminar la animación.
- **Salida estándar en `gaanim check`:** los `print()` del script no aparecen en la salida del
  comando, lo que dificulta depurar.
- **`Playable`:** es un alias solo del stub; `from gaanim.gaanim_core import Playable` falla en
  tiempo de ejecución. Exportarlo (o documentar el `TYPE_CHECKING`) ayudaría al tipado.
