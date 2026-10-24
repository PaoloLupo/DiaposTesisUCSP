# Guion

<!-- Cada "## nombre" es el guion de la diapositiva con ese nombre
     o el texto de scene.voiceover("nombre"). Una línea [stop] marca dónde
     avanzas. Guarda el archivo y la escena se actualiza. -->

## Portada
Buenas tardes al jurado, la que presenta Pamela Banda y Paolo Guillen. Vamos a hacer la sustentación de la tesis titulada Marco de trabajo para la automatización del diseño de la distribución de muros para edificios de albañilería confinado.

[stop portada]

## problematica · 1 · 1 · Índice

Para lo cual empezamos brindando contexto sobre la problemática y la importancia del diseño de la distribución de muros de albañilería confinada.

[stop entrada-problematica]

## problematica · 1 · 2 · Problemática · material

En el ultimo censo hecho por el Instituto Nacional de Estadistica e Informatica INEI se puede observar que la gran mayoria de viviendas estan hechas con ladrillos o bloques de concreto, mas precisamente un 61.8% de las viviendas del Perú tienen paredes de ladrillo o bloques de concreto, se puede a traves de este dato de estadistica suponer que de ese 61% existe una gran cantidad de viviendas que usaron la albaniñeria como sistema constructivo

[stop material-predominante]
En este grafico se desglosa los resultados con respecto al material predominante en paredes de las viviendas y con ello podemos visualmente verificar que la gran mayoria de estas es ladrillo, con lo cual la relevancia de la albañileria confinada y el hecho de que de esa mayoria, gran parte de estas viviendas han sido autoconstruidas, sin un apoyo técnico presente, quiere decir que no se esta aplicando de manera correcta la normativa para estos sistemas constructivos. Y esta falta de mano técnica en estas construcciones se agrava si consideramos el siguiente punto.

[stop materiales-listo]

## problematica · 1 · 3 · Problemática · país sísmico

Nuestra ubicación geográfica es la que se puede observar, en medio de dos placas tectónicas la de nazca y sudamericana que naturalmente se estan moviendo y

[stop dos-placas]
por el mecanismo de subducción y acumulación de energía de estas placas, ha liberado esta energía en forma de sismos a lo largo de toda nuestra historia 

[stop subduccion]
En las últimas decadas se vivieron grandes eventos sismicos como la de ancash, lima, pisco y arequipa, y ademas  se puede observar que debido a esas placas es que los terremotos con mayor grado de intensidad se dieron en nuestra costa y justamente en la costa hay mayor densidad poblacional.

[stop pais-sismico]

## problematica · 1 · 4 · Problemática · sistema sísmico

60 s. La albañilería confinada llegó tras el terremoto de Lima de 1940. (1) Seguir la obra en orden: cimiento y sobrecimiento; el acero de las columnas se ancla antes del muro; el muro se asienta con los extremos dentados; luego se vacían las columnas contra el dentado y, al final, la viga solera junto con la losa (Gonzales, 1992; San Bartolomé, 2018). Puerta y ventana llevan columnas a los lados y dintel. (2) El sismo llega en cualquier dirección; para el análisis se descompone en sus componentes X e Y (triángulo sobre el terreno). (3) En cada componente la losa reparte la fuerza y columnas y soleras amarran cada paño: la vivienda se deforma como unidad y gana ductilidad. Cada muro resiste en su plano: en X trabaja la fachada; en Y, los muros laterales. Por eso la E.070 pide densidad mínima de muros en ambas direcciones y conexión con los confinamientos. La deformación está exagerada.

[stop proceso-constructivo]

[stop componentes-del-sismo]

[stop vivienda-en-conjunto]

## problematica · 1 · 5 · Problemática · traslado manual

1.25 min. (1) En ETABS, la lista de normas de diseño de muros es de concreto armado y extranjera (ACI, Eurocódigo, CSA, NZS...): la E.070 no está, ni ningún módulo de albañilería (§1.1). (2) Por eso el ingeniero exporta las tablas del modelo (fuerzas y propiedades de los Pier, derivas), filtra y copia a una hoja de cálculo o a Mathcad: 24 muros por 4 pisos, 96 filas por tabla y combinación. Riesgos citados en la tesis: errores de selección, transcripción, ordenamiento y verificaciones omitidas; no se midió su frecuencia. (3) En la hoja, X1 no cumple: se modifica el modelo, ETABS reanaliza, cambian los V_e de todos los muros y hay que volver a copiarlo todo; a la tercera vuelta cumple, con V_e y 0.55 V_m reales del piso 1 del modelo MCT (Tabla 35, p. 86). Cerrar con la pregunta de investigación.

[stop sin-e070]

[stop traslado-manual]

[stop pregunta-de-investigacion]

## objetivos · 1 · 1 · Índice

Bloque 2 de 8: Objetivos y método. Pregunta guía: ¿Qué se propuso y cómo se evaluó? Transición breve, 5-10 s.

[stop entrada-objetivos]

## objetivos · 1 · 2 · Objetivos · general e hipótesis

60 s. Cuatro pausas. (1) Leer el objetivo general completo (§1.3.1). (2) Subrayar sus claves: marco de trabajo, automatización, albañilería confinada, norma E.070, interactuar, ETABS. (3) Esas palabras bajan y se relacionan en la hipótesis (§1.4): un marco automatizado, integrado con ETABS por su API, permitirá extraer y procesar los datos del modelo y ejecutar y documentar las verificaciones normativas, en albañilería confinada. (4) Variables (§1.5): método de diseño (manual o automatizado) y cumplimiento normativo.

[stop objetivo-general]

[stop palabras-clave]

[stop hipotesis]

[stop variables]

## objetivos · 1 · 3 · Objetivos · específicos

30 s. Cada objetivo específico tiene un producto concreto en la tesis: el flujo manual (cap. 5), los diagramas de flujo del marco (cap. 6), el programa Alba conectado por API (cap. 7) y la comparación de modelos del caso (cap. 8). Los bloques siguientes recorren estos productos en el mismo orden.

[stop objetivos-especificos]

## objetivos · 1 · 4 · Objetivos · metodología

60 s. Cinco pausas, una por etapa. (1) Revisión normativa: análisis documental de la E.030 (espectro, sismo) y la E.070 (muro confinado). (2) Diagramas de flujo: cada verificación es proceso, decisión e iteración; si no cumple se vuelve a proponer la distribución. (3) Programa propio: Alba (Python) lee el modelo de ETABS por su API, procesa y redacta el reporte en Typst. (4) Comparación descriptiva: MCT frente a MSTA aísla la idealización (misma norma); MSTA frente a MSTO aísla la norma (misma idealización). (5) Todo sobre un caso: San Bartolomé (2006), muestra no probabilística. Nivel aplicativo y enfoque cuantitativo; no es una validación estadística.

[stop metodo-normas]

[stop metodo-diagramas]

[stop metodo-programa]

[stop metodo-comparacion]

[stop metodologia]

## fundamentos · 1 · 1 · Índice

Bloque 3 de 8: Fundamentos. Pregunta guía: ¿Qué exige la norma a una distribución de muros? Transición breve, 5-10 s.

[stop entrada-fundamentos]

## fundamentos · 1 · 2 · Fundamentos · densidad

1.5 min. E.070 art. 19.2b. Con la planta real del caso: D_mín = ZUSN/56 = 3.21 % (Z = 0.45, U = S = 1, N = 4). En X se suman L·t de cada muro (X2 es de concreto y usa t_eq = t·Ec/Em = 0.794 m): Σ = 6.56 m², D_X = 4.80 %. En Y: Σ = 5.11 m², D_Y = 3.74 %. A_p = 136.51 m². Ambas cumplen; Y está más ajustada. Fuente: Tabla 22 (p. 57). Cumplir densidad no acredita las demás verificaciones.

[stop densidad-planta]

[stop densidad-formula]

[stop densidad-x]

[stop densidad-y]

[stop densidad-conclusion]

## fundamentos · 1 · 3 · Fundamentos · resistencia

1.5 min. Tres preguntas distintas. Axial (art. 19.1b): X7 del piso 1 en MCT, σ_m = 86.0 tonf/m² = 8.60 kgf/cm² frente a 9.38 kgf/cm² (92 %), el muro más exigido del modelo. Fisuración con sismo moderado (art. 26.2): X1, V_e = 7.03 frente a 0.55 V_m = 10.47 tonf. Resistencia global con sismo severo (art. 26.3): piso 1 X-X, ΣV_m = 203.0 frente a V_E = 149.8 tonf. Una verificación global favorable no prueba el cumplimiento local, y viceversa.

[stop verificacion-1]

[stop verificacion-2]

[stop verificacion-3]

[stop verificaciones-fuente]

## fundamentos · 1 · 4 · Fundamentos · deriva

1 min. Primero ambos pisos se mueven igual: Δu = 0 entre ellos. Después solo sube el desplazamiento superior; la cota terracota es Δu, se amplifica con c y se divide entre h. El dibujo está exagerado y no es una solución FEM. Límite E.030 para albañilería: 0.005. En el caso MCT la máxima es 0.00133 (Y, piso 3), 27 % del límite (Tabla 52 (p. 131)).

[stop deriva-movimiento-comun]

[stop deriva-lectura]

## fundamentos · 1 · 5 · Fundamentos · estado del arte

45 s. Cap. 3 en una línea de tiempo. Arriba, décadas de investigación experimental en albañilería confinada, casi toda de la PUCP: primera norma (1982), refuerzo y columnas (1985), esbeltez con elementos finitos (1997), la E.070 vigente y el ejemplo de San Bartolomé que es nuestro caso (2006). Abajo, desde 2019 la automatización con Python y la API de ETABS (Tabla 6, p. 32): vigas y columnas en Vietnam, irregularidades con la NSR-10, análisis sísmico E.030. La tesis une ambas líneas: la API aplicada a la E.070.

[stop estado-albanileria]

[stop estado-automatizacion]

[stop estado-tesis]

## manual · 1 · 1 · Índice

Bloque 4 de 8: Proceso manual. Pregunta guía: ¿Cómo se verifica hoy un edificio de albañilería? Transición breve, 5-10 s.

[stop entrada-manual]

## manual · 1 · 2 · Proceso manual · caso de estudio

45 s. Caso: 'Ejemplo de aplicación de la Norma E.070' de San Bartolomé (2006), resuelto originalmente con la E.030-2003 y SAP2000. Lima, cascajo, vivienda de 4 pisos, losa maciza de 12 cm, muros de 13 cm, f'm = 65 kgf/cm², f'c = 175 kgf/cm². La planta muestra las etiquetas Pier del modelo de ETABS; ′ indica el muro simétrico (_2). X2 son muros de concreto en el eje A para controlar la torsión.

[stop caso-datos]

[stop caso-x2]

## manual · 1 · 3 · Proceso manual · modelo completo en ETABS

1.5 min. El MCT se arma en ETABS 22 siguiendo sus menús: Definir, Dibujar y Asignar (§5.3.1). (1) Grillas en los ejes del plano y cuatro pisos: 2.46 m y 3 × 2.52 m. (2) Materiales: albañilería ALB65 tipo Masonry (Em = 500 f'm, ν = 0.25, γ = 1800 kgf/m³) y concreto C175 (Ec = 15 000√f'c, ν = 0.15). (3) Secciones: columnas y vigas como frames; muros M13 y P13 como shell-thin (membrana y placa); losa maciza LM12 como membrane (E.030, art. 30.8). (4) Se dibuja de nodo a nodo; con Similar Stories cada elemento aparece en los cuatro pisos, y los bordes de los shells caen sobre los frames. (5) Ocultando las losas se ve la malla de 0.50 m (Wall Auto Mesh): sus nodos coinciden con los de columnas y vigas; los brazos rígidos se asignaron a mano (End Length Offsets, factor 0.5). (6) Diafragma rígido D1 en cada losa. (7) Etiquetas Pier: un nombre por muro, igual en todos los pisos; con ellas ETABS integra los esfuerzos de la malla en fuerzas por muro. (8) Load Sets: CM 0.10 y CV 0.20 tonf/m² (azotea CV 0.10); masa = CM + 25 % CV: 121.3 tonf por piso típico y 87.8 en la azotea. Al analizar, el modo 3 (T = 0.171 s) es la traslación pura en Y; la deformada está exagerada. Dibujo esquemático: el orden de los clics es ilustrativo.

[stop mct-grillas]

[stop mct-propiedades]

[stop mct-dibujo]

[stop mct-malla]

[stop mct-diafragma]

[stop mct-pier]

[stop mct-analisis]

## manual · 1 · 4 · Proceso manual · pórticos planos

1.5 min. Modelo simplificado (MSTA), §5.3.2, con el método de San Bartolomé (2006). Antes de abrir ETABS, cada muro se prepara a mano. (1) Sección transformada en CAD con la rutina SECTRANS: las columnas de concreto se convierten en albañilería multiplicando su espesor por n = Ec/Em ≈ 6.1 y los muros transversales entran como alas. (2) La rutina une las piezas y da centroide y propiedades: X4 tiene su centroide a 1.212 m de la cara, no al centro, porque el ala de Y4 está en un extremo; A1 = 1.038 m², A2 = L t = 0.403 m², I3 = 1.509 m⁴ (Tabla 26). (3) Método del sobre: líneas a 45° reparten cada paño; X4 recibe 3.38 + 3.64 = 7.02 m², CM = 2.72 y CV = 1.40 tonf por piso; en el modelo se escalan para sumar el peso total de la losa (2.91 y 1.50 tonf). (4) En ETABS, una barra por muro en su centroide, empotrada en la base. (5) Brazos rígidos (material rígido) del centroide al borde del muro y dinteles T (interiores) o L (perimetrales): cada eje forma un pórtico plano, como el del eje A. (6) Secciones General con las propiedades calculadas; rigidez casi nula fuera del plano (× 0.0001) y peso × A2/A1 para no contar las alas. (7) Las cargas tributarias entran como fuerzas en cada barra y piso. (8) El diafragma rígido D1 une los pórticos. Contraste con el MCT: aquí la idealización y las cargas las decide el ingeniero fuera del programa.

[stop pp-seccion]

[stop pp-tributarias]

[stop pp-porticos]

[stop pp-secciones]

[stop pp-diafragma]

## manual · 1 · 5 · Proceso manual · criterios de modelamiento

1 min. Las cuatro comparaciones del cap. 4, cada una frente a su modelo de referencia (peso sísmico, fuerza sísmica y deriva; el apoyo también momentos). (1) Malla: el muro de prueba se analizó con mallas N2 a N32; entre N8 y N16 la deriva varía 0.01 %, así que basta N8 de 0.5 m. (2) Apoyo: empotrar no cambia peso ni fuerzas, la deriva baja hasta 2.63 % y el momento sube hasta 1.89 %; sin estudio de suelos basta el apoyo simple. (3) Sin columnas ni vigas de confinamiento: el peso y el cortante basal bajan 5.96 % y la deriva sube hasta 38.50 %. (4) Opciones automáticas de ETABS (inserción, brazos rígidos, malla): peso igual, deriva hasta 10.53 % menor, un modelo más rígido y no conservador.

[stop criterios-modelamiento]

## manual · 1 · 6 · Proceso manual · ciclo iterativo

45 s. Figura 41 (p. 80): modelo → exportar y filtrar tablas → copiar a hojas → verificar. Si algo no cumple, se busca el origen, se modifica el modelo y se repite todo. Decir de palabra las ocho verificaciones de la hoja: espesor efectivo, esfuerzo axial, densidad, fisuración, corte global, derivas, refuerzo horizontal y agrietamiento diagonal. En terracota, los dos pasos de transcripción a mano. El contador es ilustrativo: la tesis no registró cuántas iteraciones tomó el caso.

[stop ciclo-manual]

[stop ciclo-repeticion]

## marco · 1 · 1 · Índice

Bloque 5 de 8: Marco de trabajo. Pregunta guía: ¿Qué se automatiza y con qué lógica? Transición breve, 5-10 s.

[stop entrada-marco]

## marco · 1 · 2 · Marco · qué se automatiza

45 s. Criterios de proceso clave (cap. 6): se repite, muchos datos con la misma estructura, expuesto a transcripción, criterio normativo explícito, produce información para la revisión. Cuatro procesos: extracción, verificación, evaluación con retroalimentación y reportes. El marco no genera la estructuración ni modifica la distribución: esas decisiones siguen en el ingeniero.

[stop criterios-procesos-clave]

[stop reparto]

## marco · 1 · 3 · Marco · flujo general

1 min. Figura 42 (p. 103). Antes de verificar se valida: una etiqueta, combinación o parámetro faltante detiene el módulo con un diagnóstico, y eso no es un incumplimiento normativo. Luego se procesa por muro, piso y dirección, se ejecutan los módulos y se consolidan resultados. Si el ingeniero modifica el modelo, se vuelve a analizar y a importar; si no, se genera el reporte.

[stop flujo-importacion]

[stop flujo-general]

## marco · 1 · 4 · Marco · módulo de densidad

1.5 min. Figura 43 (p. 105) como ejemplo de módulo: entradas, validación, clasificación, aporte efectivo (concreto con Ec/Em), suma, comparación y salida. A la derecha, los valores del caso en cada paso. Luego tres pasadas rápidas, unos 5 s cada una y sin recorrerlas: esfuerzo axial (Fig. 44), fisuración y corte (Fig. 45, por muro y luego por entrepiso) y derivas (Fig. 46). Basta decir que siguen la misma estructura: datos, validación, cálculo, decisión y salida.

[stop modulo-densidad]

[stop modulo-recorrido]

[stop modulo-axial]

[stop modulo-corte]

[stop modulo-derivas]

## marco · 1 · 5 · Marco · entradas, salidas y trazabilidad

45 s. Entradas separadas: lo que se lee del modelo por API y lo que declara el usuario. Salidas: interfaz y PDF de la misma iteración. El registro de ejemplo es la resistencia global del piso 1 en X-X del modelo MCT: V_E = 149.805 tonf y ΣV_m = 203.032 tonf. Es un agregado de piso, no un Pier individual.

[stop entradas-salidas]

[stop trazabilidad]

## alba · 1 · 1 · Índice

Bloque 6 de 8: Implementación: Alba. Pregunta guía: ¿Cómo se conecta el marco con ETABS? Transición breve, 5-10 s.

[stop entrada-alba]

## alba · 1 · 2 · Alba · arquitectura

45 s. Seis módulos (cap. 7): interfaz (ImGui Bundle), gestión del proyecto (archivo .alb), conexión con ETABS por COM (comtypes), procesamiento (pandas: filtrar, clasificar por Pier y dirección), verificaciones normativas y visualización/reportes (Typst, openpyxl). El recorrido del punto sigue un dato desde ETABS hasta el PDF. Alba es de código libre.

[stop arquitectura-modulos]

[stop arquitectura-flujo]

## alba · 1 · 3 · Alba · API de ETABS

45 s. Tabla 47 (p. 120): métodos consultados para niveles, materiales, muros, elementos de área y frame, conectividad, tablas de resultados y control del análisis. Esto reemplaza la exportación manual de tablas. Antes de leer se comprueba que exista una instancia abierta y un modelo analizado; si no, la consola advierte.

[stop api-etabs]

## alba · 1 · 4 · Alba · interfaz

45 s. Captura real (Figura 51 (p. 121)) con el modelo del caso: 136.51 m², 4 pisos, zona 4. Barra de herramientas; panel de flujo con estado de conexión y etapas (proyecto, muros, verificaciones, capturas, reporte); panel de trabajo; consola de diagnósticos. No es una demostración en vivo.

[stop interfaz-zona-1]

[stop interfaz-zona-2]

[stop interfaz-zona-3]

[stop interfaz]

## alba · 1 · 5 · Alba · reporte

30 s. Python procesa y exporta un JSON; la plantilla Typst compone el PDF con fórmulas, tablas, referencias normativas y capturas. El fragmento corresponde a la densidad mínima (0.032) del caso.

[stop reporte-fragmento]

[stop reporte-cadena]

## alba · 1 · 6 · Alba · partes del reporte

30 s. El reporte real del caso (anexo, 21 páginas) con sus seis secciones de la Tabla 48 (p. 124). Arriba están sus páginas, agrupadas por sección; en cada pausa se abre una en el índice y se acerca una de sus páginas.

[stop reporte-partes]
Datos de diseño: geometría, niveles, materiales y parámetros sísmicos (pp. 3–5).

[stop reporte-parte-1]
Requisitos mínimos: espesor efectivo t = 0.12 m y densidad mínima de 0.032 en cada dirección (pp. 6–7).

[stop reporte-parte-2]
Carga vertical: esfuerzo axial por cargas de gravedad, muro por muro (pp. 8–10).

[stop reporte-parte-3]
Análisis sísmico: peso, modos, fuerzas y derivas; la página muestra la deriva en X (pp. 11–14).

[stop reporte-parte-4]
Sismo moderado: fisuración y resistencia al corte global, la parte más larga (pp. 15–20).

[stop reporte-parte-5]
Información del modelo: versión de la API, archivo y fecha de importación, la trazabilidad de la iteración (p. 21).

[stop reporte-parte-6]

## resultados · 1 · 1 · Índice

Bloque 7 de 8: Resultados. Pregunta guía: ¿Qué muestran los tres modelos del caso? Transición breve, 5-10 s.

[stop entrada-resultados]

## resultados · 1 · 2 · Resultados · modelos comparados

45 s. MCT: modelo completo en ETABS procesado con Alba. MSTA: pórticos planos actualizados, ETABS + hojas de cálculo. MSTO: referencia de San Bartolomé (2006) en SAP2000 con E.030-2003. La lógica de lectura: MCT vs MSTA aísla la idealización y el procesamiento (misma norma); MSTA vs MSTO aísla la norma (misma idealización). La comparación es descriptiva: no mide una tasa de error de Alba.

[stop modelos-matriz]

[stop modelos-logica]

## resultados · 1 · 3 · Resultados · peso y fuerzas

1 min. Tabla 50 (p. 129): 451.84 / 456.57 / 432.11 tonf. MSTA pesa 1.04 % más que MCT (áreas tributarias vs volumen modelado); MSTO pesa 5.66 % menos que MSTA por columnas de 0.20 m. Tabla 51 (p. 130): Fi difiere a lo más 2.14 % entre MCT y MSTA, pero MSTO es hasta 23.3 % menor que MSTA en el piso 4 por el cambio de Z y de la E.030.

[stop peso-sismico]

[stop fuerzas-altura]

## resultados · 1 · 4 · Resultados · derivas

1 min. Primer encuadre con el límite 0.5 %: todas las derivas quedan lejos. Detalle 0–0.2 %: MCT (áreas) es más rígido; hasta 13.65 % menor que MSTA en X piso 4 y 32.7 % menor que MSTO. Excepción: piso 1, MCT supera ligeramente a MSTA (X 0.000913 vs 0.000884; Y 0.000987 vs 0.000977). La mayor rigidez de MSTA frente a MSTO se atribuye a las columnas de 0.25 m.

[stop derivas-limite]

[stop derivas-detalle]

## resultados · 1 · 5 · Resultados · cortante

45 s. Tabla 53 (p. 133). En Y, MCT es hasta 11.25 % menor que MSTA: el modelo de áreas considera el aporte de muros ortogonales. En X ambos casi coinciden porque los confinamientos de intersecciones T/L se asignaron al Pier de la dirección X (limitación de ETABS: un elemento no pertenece a dos Pier). MSTO es hasta 30.9 % menor en X por la E.030-2003.

[stop cortante]

## resultados · 1 · 6 · Resultados · resistencia global

1.25 min. Cociente V_E / ΣV_m por piso: todo por debajo de 1 salvo MSTA, piso 1, X-X: 151.213 / 146.756 = 1.030, que la hoja de cálculo marca como 'No cumple · replantear'. MCT obtiene 203.032 tonf (38 % más) porque el metrado automático da una P_g más representativa y la losa redistribuye cargas. El diagnóstico depende del modelo.

[stop resistencia-grafico]

[stop resistencia-diagnostico]

## conclusiones · 1 · 1 · Índice

Bloque 8 de 8: Conclusiones. Pregunta guía: ¿Qué aporta el trabajo y qué queda abierto? Transición breve, 5-10 s.

[stop entrada-conclusiones]

## conclusiones · 1 · 2 · Conclusiones · objetivos

1 min. Retomar cada objetivo específico con su conclusión (Conclusiones, p. 135). La hipótesis se sostiene para el caso: el marco integra de forma reproducible extracción, procesamiento, verificación y documentación. No se afirma una reducción medida de tiempo o de errores: no se midió.

[stop objetivos-cumplidos]

## conclusiones · 1 · 3 · Conclusiones · hallazgos

1 min. Lo que dicen las Conclusiones (pp. 135–136). (1) El MCT reduce conservadurismo innecesario y da más detalle: las áreas reparten mejor la carga de losa y cuentan el aporte de los muros ortogonales. (2) La E.030 vigente es más rigurosa que la de 2003: combinación direccional 100 % + 30 % y factores sísmicos mayores. (3) Las columnas de 0.25 m de la propuesta E.070 reducen las derivas hasta 22.61 % y neutralizan esa exigencia. (4) Alba es una herramienta de apoyo de código libre. Cerrar con el criterio del usuario como factor determinante.

[stop hallazgos]

## conclusiones · 1 · 4 · Conclusiones · recomendaciones

45 s. Recomendaciones (p. 137): modelos completos con elementos área, fuerzas en intersecciones T y L (un confinamiento solo puede tener una etiqueta Pier), diseño de confinamientos en Alba, mantenimiento del código libre con el RNE, análisis no lineal con macromodelos, CNN para irregularidades en planta y uso educativo.

[stop recomendaciones]

## conclusiones · 1 · 5 · Cierre

Agradecer y abrir la ronda de preguntas. Mantener esta diapositiva durante la discusión.

[stop preguntas]
