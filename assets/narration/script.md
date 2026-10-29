# Guion

<!-- Cada "## nombre" es el guion de la diapositiva con ese nombre
     o el texto de scene.voiceover("nombre"). Una línea [stop] marca dónde
     avanzas. Guarda el archivo y la escena se actualiza. -->

## Portada
Buenas tardes al jurado, el que presenta Paolo Guillen y Pamela Banda. Vamos a hacer la sustentación de la tesis titulada Marco de trabajo para la automatización del diseño de la distribución de muros para edificios de albañilería confinada.

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

Frente a este peligro sísmico, el sistema constructivo que predomina en nuestras viviendas es la albañilería confinada, que se empezó a usar en el Perú después del terremoto de Lima de 1940. Para entender cómo trabaja seguimos su proceso constructivo: primero el cimiento y el sobrecimiento; luego se ancla el acero de las columnas, antes de asentar el muro; después se levanta el muro de ladrillo hilada por hilada, dejando los extremos dentados, como se puede observar en la esquina; luego se vacían las columnas, y el concreto llena ese dentado y amarra el muro; y al final se vacían juntas la viga solera y la losa, con lo cual se cierra el confinamiento.

[stop proceso-constructivo]
Ahora, cuando ocurre un sismo, este no llega en una dirección fija, puede venir en cualquier dirección. Por eso, para el análisis se idealiza descomponiéndolo en sus dos componentes, una en X y otra en Y, como se ve en el triángulo sobre el terreno.

[stop componentes-del-sismo]
En cada una de estas direcciones la losa reparte la fuerza entre todos los muros como un diafragma rígido, y las columnas y vigas soleras amarran cada paño, con lo cual la vivienda se deforma como una unidad. Pero cada muro resiste en su plano: en X trabaja la fachada y en Y trabajan los muros laterales. Por eso la norma E.070 exige una densidad mínima de muros en ambas direcciones y una buena conexión con los confinamientos. La deformación que se ve está exagerada.

[stop vivienda-en-conjunto]

## problematica · 1 · 5 · Problemática · traslado manual

Para analizar estas edificaciones, uno de los programas más usados es ETABS. Sin embargo, si revisamos las normas que ofrece para el diseño de muros, todas son de concreto armado y extranjeras: la ACI, el Eurocódigo, la canadiense, la neozelandesa, entre otras. La norma E.070 no está implementada, ni ningún módulo de albañilería, con lo cual la verificación queda fuera del programa y se tiene que resolver a mano en hojas de cálculo.

[stop sin-e070]
¿Y cómo se hace eso a mano? El ingeniero exporta las tablas del modelo, como las fuerzas de cada muro, las propiedades de las secciones y las derivas, las filtra y las copia a una hoja de cálculo o a Mathcad. Para darnos una idea, en este edificio son 24 muros de albañilería en 4 pisos, quiere decir 96 filas por cada tabla y por cada combinación. Y en este traslado se corre el riesgo de cometer errores de selección, de transcripción, de ordenamiento, o de omitir alguna verificación.

[stop traslado-manual]
Además, el proceso no termina en una sola pasada. Si en la hoja un muro no cumple, como aquí el muro X1, se modifica el modelo, ETABS vuelve a analizar, cambian las fuerzas de todos los muros y hay que volver a copiar todo. En este ejemplo el muro recién cumple a la tercera vuelta, y los valores de esa última vuelta son los reales del primer piso de nuestro modelo. De aquí nace nuestra pregunta de investigación: ¿cómo sistematizar la verificación de la norma E.070 a partir de un modelo de ETABS?

[stop pregunta-de-investigacion]

## objetivos · 1 · 1 · Índice

Con esto pasamos al segundo bloque, los objetivos y el método: qué nos propusimos y cómo lo evaluamos.

[stop entrada-objetivos]

## objetivos · 1 · 2 · Objetivos · general e hipótesis

Nuestro objetivo general es desarrollar un marco de trabajo para la automatización del diseño de la distribución de muros en planta para edificios de albañilería confinada, conforme a los requerimientos de la norma E.070, y su aplicación mediante un programa de desarrollo propio capaz de interactuar con el software comercial ETABS.

[stop objetivo-general]
De este objetivo resaltamos sus palabras clave: un marco de trabajo, la automatización, la albañilería confinada, la norma E.070, y que el programa debe interactuar con ETABS.

[stop palabras-clave]
Estas mismas palabras forman nuestra hipótesis: si se implementa un marco de trabajo automatizado, integrado con ETABS mediante su API, esto permitirá que las verificaciones normativas se ejecuten y se documenten de forma sistemática, en edificaciones de albañilería confinada.

[stop hipotesis]
Con lo cual se definen dos variables: la variable independiente es el método de diseño, que pasa de manual a automatizado, y la variable dependiente es el cumplimiento normativo.

[stop variables]

## objetivos · 1 · 3 · Objetivos · específicos

Para lograr el objetivo general planteamos cuatro objetivos específicos, y cada uno tiene un producto en la tesis. Primero, identificar el proceso manual de diseño, que se desarrolla en el capítulo 5. Segundo, desarrollar el marco de trabajo con diagramas de flujo, en el capítulo 6. Tercero, aplicar el marco en un programa que interactúa con ETABS por su API, que es Alba, en el capítulo 7. Y cuarto, evaluar los resultados del caso comparando alternativas de modelamiento, en el capítulo 8. La presentación sigue este mismo orden.

[stop objetivos-especificos]

## objetivos · 1 · 4 · Objetivos · metodología

Nuestra investigación tiene 4 objetivos especifico. La primera es la revisión normativa (identificar): el análisis de la norma E.030, de donde sale el espectro de diseño sísmico, y de la norma E.070, que define cómo se verifica el muro confinado.

[stop metodo-normas]
La segunda son los diagramas de flujo, donde cada verificación se representa con procesos, decisiones e iteraciones: si algo no cumple se vuelve atrás y se propone otra distribución, y si cumple se continúa.

[stop metodo-diagramas]
La tercera es el programa de desarrollo propio, Alba, hecho en Python que apica el marco de trabajo ya realizado y que lee del modelo de ETABS mediante su API la geometría, las cargas y las fuerzas de cada muro, hace las verificaciones y redacta el reporte automatizado en PDF.

[stop metodo-programa]
La cuarta es una comparación descriptiva de un mismo edificio en tres modelos: el Modelo completo tridimensional, con los muros como áreas, y el Modelo Simplificado Tridimensional Actualizado y el Modelo Simplificado Tridimensional Original, con los muros como barras. Entre el Modelo completo tridimensional y el MSTA la norma es la misma, así que lo que cambia es la idealización; y entre el MSTA y el MSTO la idealización es la misma y lo que cambia es la norma.

[stop metodo-comparacion]
Todo esto se aplicó sobre un caso de estudio, un edificio de albañilería confinada de 4 pisos del ejemplo de San Bartolomé del 2006, que es una muestra no probabilística. Por eso la investigación es de nivel aplicativo y enfoque cuantitativo, y no pretende ser una validación estadística.

[stop metodologia]

## fundamentos · 1 · 1 · Índice


[stop entrada-fundamentos]

## fundamentos · 1 · 2 · Fundamentos · densidad


[stop densidad-planta]

[stop densidad-formula]

[stop densidad-x]

[stop densidad-y]

[stop densidad-conclusion]

## fundamentos · 1 · 3 · Fundamentos · resistencia

La norma también exige tres verificaciones de resistencia, y cada una responde a una pregunta distinta. La primera es por cargas gravitatorias: ¿la compresión en el muro es admisible? Se calcula el esfuerzo axial como la carga entre el área del muro y se compara con el límite de la norma. En nuestro caso el muro más exigido es el X7 del primer piso, con 8.60 kilogramos por centímetro cuadrado frente a un límite de 9.38, es decir al 92 % del límite, y cumple.

[stop verificacion-1]
La segunda es para sismo moderado: ¿se evita la fisuración por corte del muro? Aquí el cortante del sismo, Ve, debe ser menor o igual al 55 % de la resistencia al corte del muro, Vm. Por ejemplo, en el muro X1 del primer piso Ve es 7.03 toneladas frente a 10.47, por lo que cumple.

[stop verificacion-2]
La tercera es para sismo severo, y ya no es por muro sino por piso: ¿los muros del piso resisten en conjunto? La suma de las resistencias de los muros debe ser mayor o igual al cortante del entrepiso. En el primer piso, en la dirección X, la suma es 203 toneladas frente a una demanda de 149.8, y cumple.

[stop verificacion-3]
Algo importante es que estas verificaciones son independientes: que el piso cumpla en conjunto no garantiza que cada muro cumpla, y lo mismo al revés.

[stop verificaciones-fuente]

## fundamentos · 1 · 4 · Fundamentos · deriva

La última exigencia es la deriva, que es el desplazamiento relativo entre pisos. Como se puede observar en este esquema, cuando ambos pisos se desplazan lo mismo no hay deriva entre ellos, porque la diferencia de desplazamientos es cero.

[stop deriva-movimiento-comun]
En cambio, cuando el piso superior se desplaza más aparece una diferencia, delta u. Esa diferencia se amplifica con el factor c, que depende del coeficiente de reducción R, y se divide entre la altura del entrepiso, y el resultado no debe pasar de 0.005, que es el límite de la E.030 para albañilería. En nuestro caso la deriva máxima del modelo completo es 0.00133, en la dirección Y del tercer piso, apenas el 27 % del límite. El dibujo está exagerado.

[stop deriva-lectura]

## fundamentos · 1 · 5 · Fundamentos · estado del arte

En cuanto al estado del arte, lo podemos ver en una línea de tiempo. Arriba está la investigación en albañilería confinada, que tiene décadas y en su mayoría se desarrolló en la PUCP: desde la primera norma de 1982, los estudios de refuerzo y columnas, la esbeltez con elementos finitos, hasta la norma E.070 del 2006 junto con el ejemplo de San Bartolomé, que es nuestro caso de estudio.

[stop estado-albanileria]
Abajo está una línea más reciente: desde el 2019 aparecen trabajos de automatización con Python y con la API de ETABS, por ejemplo para el diseño de concreto armado, para evaluar irregularidades con la norma colombiana NSR-10 y para el análisis sísmico con la E.030.

[stop estado-automatizacion]
Nuestra tesis se ubica en la unión de ambas líneas: aplica la API de ETABS con Python a la verificación de la norma E.070 de albañilería.

[stop estado-tesis]

## manual · 1 · 1 · Índice

Con esto pasamos al cuarto bloque, el proceso manual, donde mostramos cómo se verifica hoy un edificio de albañilería.

[stop entrada-manual]

## manual · 1 · 2 · Proceso manual · caso de estudio

El caso de estudio es el ejemplo de aplicación de la norma E.070 del ingeniero Ángel San Bartolomé, del 2006, que originalmente se resolvió con la E.030 del 2003 y con SAP2000. Es una vivienda de 4 pisos en Lima, sobre suelo rígido, de cascajo, con una planta de 16.6 por 8 metros, losa maciza de 12 centímetros, muros de 13 centímetros, albañilería con un f'm de 65 y concreto con un f'c de 175 kilogramos por centímetro cuadrado. En la planta se ven los nombres de cada muro, que son las etiquetas Pier que usamos en ETABS; el apóstrofe indica el muro simétrico.

Un detalle importante son los muros X2, que son de concreto armado y están en el eje A para acercar el centro de rigidez al centro de masas y así controlar la torsión.

[stop caso-estudio]

## manual · 1 · 3 · Proceso manual · modelos comparados

Comparamos tres modelos del mismo edificio. El MCT es el modelo completo tridimensional en ETABS, con los muros como áreas y procesado con Alba. El MSTA es el modelo simplificado actualizado, de pórticos planos, también en ETABS y con la norma vigente, pero procesado con hojas de cálculo. Y el MSTO es el modelo simplificado original de San Bartolomé, hecho en SAP2000 con la E.030 del 2003, que usa un factor de zona de 0.40, no considera el sismo ortogonal y tiene columnas de 0.20 metros.

[stop modelos-matriz]
La lectura es la siguiente: entre el MCT y el MSTA la norma es la misma, así que la diferencia viene de la idealización y del procesamiento; y entre el MSTA y el MSTO la idealización es la misma, así que la diferencia viene de la norma. Es una comparación descriptiva, no mide una tasa de error de Alba.

[stop modelos-logica]

## manual · 1 · 4 · Proceso manual · modelo completo en ETABS

Ahora mostramos cómo se arma el modelo completo, el MCT, en ETABS, siguiendo sus menús: definir, dibujar y asignar. Primero se definen las grillas según los ejes del plano y los cuatro pisos, el primero de 2.46 metros y los demás de 2.52.

[stop mct-grillas]
Luego se definen los materiales, la albañilería con un módulo de elasticidad de 500 f'm y el concreto, y después las secciones: las columnas y vigas como frames, los muros como shell-thin y la losa maciza como membrana.

[stop mct-propiedades]
Con eso se dibuja de nodo a nodo: columnas, vigas, muros y losas, y con la opción de pisos similares cada elemento aparece en los cuatro pisos a la vez.

[stop mct-dibujo]
Después se asigna una malla de 0.50 metros en cada muro. Si nos acercamos a una unión, se puede observar que los nodos de la malla coinciden con los de las columnas y vigas, y que los brazos rígidos en la cara de la columna se asignaron a mano.

[stop mct-malla]
Luego se asigna un diafragma rígido en cada losa, de modo que cada piso se mueve como un sólido.

[stop mct-diafragma]
Y se asignan las etiquetas Pier, un nombre por muro, el mismo en los cuatro pisos. Con estas etiquetas ETABS integra los esfuerzos de la malla y nos da las fuerzas de cada muro, que son las que se usan en las verificaciones.

[stop mct-pier]
Por último se asignan las cargas: una carga muerta de 0.10 y una carga viva de 0.20 toneladas por metro cuadrado, y 0.10 en la azotea. La masa se toma como la carga muerta más el 25 % de la viva, lo que da 121.3 toneladas por piso típico y 87.8 en la azotea.

[stop mct-cargas]

## manual · 1 · 5 · Proceso manual · pórticos planos

El segundo modelo es el simplificado, el MSTA, que sigue el método de pórticos planos de San Bartolomé. Aquí, antes de abrir ETABS, cada muro se tiene que preparar a mano. Primero se obtiene su sección transformada en CAD con la rutina SECTRANS: las columnas de concreto se convierten a albañilería multiplicando su espesor por n, la relación de módulos, que es 6.1, y los muros transversales entran como alas.

[stop pp-transformada]
Por ejemplo, en el muro X4 el centroide queda a 1.212 metros de la cara y no al centro, porque el ala del muro Y4 está en un extremo, y de ahí salen su área, su área de corte y su inercia.

[stop pp-seccion]
Luego se calculan las cargas con el método del sobre, trazando líneas a 45 grados en cada paño. Al muro X4 le corresponden 7.02 metros cuadrados, lo que da 2.72 toneladas de carga muerta y 1.40 de carga viva por piso.

[stop pp-tributarias]
Ya en ETABS se dibuja una barra por muro en su centroide, empotrada en la base.

[stop pp-barras]
Luego cada barra se une con brazos rígidos hasta el borde del muro y con los dinteles. Así, cada eje forma un pórtico plano, como este del eje A.

[stop pp-porticos]
A cada barra se le asigna una sección general con las propiedades calculadas, con una rigidez casi nula fuera de su plano, y su peso se corrige para no contar dos veces el peso de las alas.

[stop pp-secciones]
Después se asignan las cargas tributarias como fuerzas en cada barra y en cada piso, que en el caso de X4 se escalan a 2.91 y 1.50 toneladas para sumar el peso total de la losa.

[stop pp-cargas]
Finalmente, el diafragma rígido une todos los pórticos. A diferencia del modelo completo, aquí la idealización y las cargas las decide el ingeniero fuera del programa.

[stop pp-diafragma]

## manual · 1 · 6 · Proceso manual · criterios de modelamiento

Además, en el capítulo 4 evaluamos cuatro criterios de modelamiento, cada uno frente a un modelo de referencia. Primero la malla: probamos desde mallas muy gruesas hasta muy finas, y a partir de 0.5 metros la deriva prácticamente ya no cambia, así que esa malla es suficiente. Segundo el apoyo: empotrar la base no cambia el peso ni las fuerzas y la deriva varía como máximo 2.63 %, así que sin un estudio de suelos basta con el apoyo simple. Tercero, si se modela sin columnas ni vigas de confinamiento, la deriva sube hasta 38.5 %. Y cuarto, si se usan las opciones automáticas de ETABS la deriva sale hasta 10.5 % menor, quiere decir un modelo más rígido, que no es conservador.

[stop criterios-modelamiento]

## manual · 1 · 7 · Proceso manual · ciclo iterativo

Juntando todo, el proceso manual es un ciclo: se modela y analiza en ETABS, se exportan y filtran las tablas, se copian a las hojas de cálculo y se verifica con la E.070 y la E.030. En la hoja se revisan ocho verificaciones: espesor efectivo, esfuerzo axial, densidad, fisuración, corte global, derivas, refuerzo horizontal y agrietamiento diagonal. En terracota están los dos pasos que se hacen a mano.

[stop ciclo-manual]
Y si algo no cumple, se cambian los muros en el modelo y se repite todo el ciclo, exportando y copiando otra vez en cada vuelta, hasta que todo cumple y recién se redacta la memoria de cálculo. El número de vueltas que se ve es ilustrativo. Justamente estos pasos repetitivos son los que buscamos automatizar.

[stop ciclo-repeticion]

## marco · 1 · 1 · Índice

Pasamos al quinto bloque, el marco de trabajo, donde explicamos qué se automatiza y con qué lógica.

[stop entrada-marco]

## marco · 1 · 2 · Marco · qué se automatiza

Para definir qué automatizar consideramos que un proceso es clave si se repite en cada iteración, si maneja muchos datos con la misma estructura, si tiene riesgo de transcripción, si su criterio normativo es explícito y si alimenta la revisión.

[stop criterios-procesos-clave]
Con esos criterios se reparte el trabajo. El ingeniero estructural sigue definiendo la distribución de muros, modela y analiza en ETABS, interpreta los resultados y decide qué cambiar. El marco, implementado en Alba, se encarga de extraer los datos por la API, de las verificaciones de la E.070 y la E.030, de señalar el muro, el piso y la dirección que no cumplen, y del reporte en PDF. Es decir, el marco no diseña la distribución: esa decisión sigue siendo del ingeniero.

[stop reparto]

## marco · 1 · 3 · Marco · flujo general

Este es el flujo general del marco. Parte de un proyecto configurado y un modelo ya analizado en ETABS, y lo primero es importar y validar los datos mediante la API. Si falta una etiqueta, una combinación o un parámetro, el módulo se detiene y muestra un diagnóstico, y eso no se reporta como un incumplimiento de la norma, sino como un dato que hay que corregir. Luego los datos se organizan por muro, piso y dirección, y se ejecutan los módulos de verificación.

[stop flujo-importacion]
Después se consolidan los resultados con sus diagnósticos. Si el ingeniero decide hacer una nueva iteración, modifica el modelo en ETABS, lo vuelve a analizar y el ciclo se repite desde la importación; si no, se genera el reporte en PDF. La diferencia con el proceso manual es que en cada vuelta ya no hay que volver a copiar las tablas a mano.

[stop flujo-general]

## marco · 1 · 4 · Marco · módulo de densidad

Cada verificación se implementa como un módulo, y como ejemplo tomamos el de densidad. Tiene sus entradas, que son los parámetros sísmicos y la tabla de muros; una validación de los datos; la clasificación de los muros por dirección y material; el cálculo del aporte de cada muro; la suma; la comparación con la densidad mínima; y la salida, que es una tabla con los muros considerados.

[stop modulo-densidad]
Si recorremos el módulo con los valores del caso: entran los parámetros sísmicos y el área de 136.51 metros cuadrados; no faltan datos, así que continúa; se clasifican 13 tramos en X y 13 en Y; los muros X2 de concreto entran con su espesor equivalente; las sumas dan 6.56 y 5.11 metros cuadrados, y las densidades 4.80 % y 3.74 % frente al mínimo de 3.21 %, con lo cual ambas direcciones cumplen. Son los mismos valores que vimos en los fundamentos.

[stop modulo-recorrido]
El módulo de esfuerzo axial sigue la misma estructura: datos por muro y nivel, validación, cálculo del esfuerzo, comparación con los límites y salida.

[stop modulo-axial]
El de fisuración y corte primero verifica cada muro y luego agrupa por entrepiso para la resistencia global.

[stop modulo-corte]
Y el de derivas ordena los niveles, calcula la distorsión de cada entrepiso y la compara con el límite de 0.005.

[stop modulo-derivas]

## marco · 1 · 5 · Marco · entradas, salidas y trazabilidad

En las entradas separamos lo que se lee de ETABS por la API, como la geometría, los materiales, los resultados y las etiquetas Pier, de lo que declara el usuario, como los parámetros sísmicos y las combinaciones a usar. Las salidas se muestran en la interfaz y en el reporte PDF de la misma iteración.

[stop entradas-salidas]
Y cada resultado conserva su origen. Por ejemplo, este registro corresponde al modelo MCT, primer piso, dirección X, resistencia global: una demanda de 149.805 toneladas frente a una resistencia de 203.032, que cumple. Así, desde el reporte se puede volver al modelo, al piso y a la dirección de cada valor.

[stop trazabilidad]

## alba · 1 · 1 · Índice

Pasamos al sexto bloque, la implementación del marco en Alba, donde vemos cómo se conecta con ETABS.

[stop entrada-alba]

## alba · 1 · 2 · Alba · el programa

Antes de entrar en detalle, les presentamos Alba. Es un programa de escritorio que desarrollamos para implementar el marco: verifica edificaciones de albañilería confinada a partir de su modelo analizado en ETABS.

[stop alba-programa]
Está escrito en Python, se conecta con ETABS mediante su API y es software libre, de modo que cualquier ingeniero puede usarlo y mejorarlo.

[stop alba-ficha]

## alba · 1 · 3 · Alba · arquitectura

Por dentro, Alba se organiza en seis módulos. Los dos primeros son de interacción con el usuario: la interfaz y la gestión del proyecto. Los otros cuatro son de procesamiento interno: la conexión con ETABS por su API, el procesamiento de datos con pandas, las verificaciones de la E.070 y la E.030, y la visualización y los reportes, con Typst y Excel.

[stop arquitectura-modulos]
Si seguimos un dato, este sale del modelo analizado en ETABS, entra por el módulo de conexión, se procesa, se verifica y termina en el reporte PDF y en las tablas de Excel.

[stop arquitectura-flujo]

## alba · 1 · 4 · Alba · API de ETABS

La conexión se hace mediante la API de ETABS. En esta tabla están los métodos que consulta Alba para obtener los niveles y sus alturas, los materiales, las propiedades de los muros, los nodos y la orientación de cada elemento área, las secciones de los frames, la conectividad, las tablas de resultados y el control del análisis. Con esto se reemplaza la exportación manual de tablas que vimos antes. Y antes de leer, Alba comprueba que haya una instancia de ETABS abierta y que el modelo esté analizado; si falta algo, la consola lo advierte y no se calcula.

[stop api-etabs]

## alba · 1 · 5 · Alba · interfaz

Esta es una captura real de la interfaz de Alba con el modelo del caso. Arriba está la barra de herramientas, desde donde se importan los datos de ETABS, se abre y se guarda el proyecto, y se generan el reporte y el Excel.

[stop interfaz-zona-1]
A la izquierda está el panel de flujo, que muestra el estado de la conexión con ETABS y las etapas del marco: proyecto, muros, verificaciones, capturas y reporte, con sus alertas.

[stop interfaz-zona-2]
Al centro está el panel de trabajo, con los parámetros del proyecto, como el área de 136.51 metros cuadrados, los 4 pisos y la zona 4, y con las tablas de muros y resultados con su estado.

[stop interfaz-zona-3]
Y abajo está la consola de diagnósticos, donde aparecen los errores de conexión y los datos faltantes o inconsistentes de la importación.

[stop interfaz]

## alba · 1 · 6 · Alba · reporte

El reporte se genera automáticamente. A la izquierda se ve un fragmento del PDF con la verificación de densidad mínima, su fórmula, sus variables y el valor de 0.032 del caso. A la derecha está la plantilla en Typst que lo produce, donde los valores no se escriben a mano, sino que llegan desde un archivo JSON.

[stop reporte-fragmento]
Es decir, Python procesa los datos y exporta los resultados a un JSON, la plantilla de Typst los toma y compone el PDF, y aparte se generan las tablas en Excel.

[stop reporte-cadena]

## alba · 1 · 7 · Alba · partes del reporte

Este es el reporte real del caso, que tiene 21 páginas organizadas en seis partes. Arriba se ven sus páginas agrupadas por parte, y a la derecha la portada.

[stop reporte-partes]
La primera parte son los datos de diseño: la geometría, los niveles, los materiales y los parámetros sísmicos.

[stop reporte-parte-1]
La segunda son los requisitos mínimos: el espesor efectivo, que da 0.12 metros, y la densidad mínima de 0.032 en cada dirección.

[stop reporte-parte-2]
La tercera es el análisis por carga vertical, con el esfuerzo axial muro por muro.

[stop reporte-parte-3]
La cuarta es el análisis sísmico: el peso, los modos, las fuerzas y las derivas; aquí se ve la gráfica de derivas en X.

[stop reporte-parte-4]
La quinta es el análisis para sismo moderado, con el control de fisuración y la resistencia al corte global, que es la parte más extensa.

[stop reporte-parte-5]
Y la sexta es la información del modelo: la versión de la API, el archivo y la fecha de importación, con lo cual se sabe de qué iteración sale cada reporte.

[stop reporte-parte-6]

## resultados · 1 · 1 · Índice

Pasamos al séptimo bloque, los resultados, donde vemos qué muestran los tres modelos del caso.

[stop entrada-resultados]

## resultados · 1 · 2 · Resultados · peso y fuerzas

Empezando por el peso sísmico, el MCT tiene 451.8 toneladas, el MSTA 456.6 y el MSTO 432.1. El MSTA pesa 1.04 % más que el MCT, porque sus cargas salen de áreas tributarias y no del volumen modelado, y el MSTO pesa 5.66 % menos, porque usa columnas de 0.20 metros.

[stop peso-sismico]
En las fuerzas sísmicas por nivel, el MCT y el MSTA difieren como máximo 2.14 %, quiere decir que la idealización casi no cambia la fuerza. En cambio, el MSTO es hasta 23.3 % menor que el MSTA en el cuarto piso, por el cambio del factor de zona y de la norma E.030. Por eso decimos que la norma pesa más que la idealización.

[stop fuerzas-altura]

## resultados · 1 · 3 · Resultados · derivas

En las derivas, si las vemos junto al límite de la E.030 de 0.5 %, en ambas direcciones los tres modelos quedan muy por debajo.

[stop derivas-limite]
Si nos acercamos, se puede observar que el MCT, al modelar los muros como áreas, es más rígido: su deriva es hasta 13.65 % menor que la del MSTA en el cuarto piso en X, y hasta 32.7 % menor que la del MSTO. La excepción es el primer piso, donde el MCT supera ligeramente al MSTA en ambas direcciones. Y la mayor rigidez del MSTA frente al MSTO se debe a sus columnas de 0.25 metros.

[stop derivas-detalle]

## resultados · 1 · 4 · Resultados · cortante

En el cortante para sismo severo, en la dirección Y el MCT es hasta 11.25 % menor que el MSTA, porque el modelo de áreas considera el aporte de los muros ortogonales. En X, en cambio, ambos casi coinciden, porque los confinamientos de las intersecciones en T y en L se asignaron a los muros en X, ya que en ETABS un elemento no puede pertenecer a dos Pier. Y frente al MSTO, la norma vigente eleva el cortante hasta 30.9 % en X.

[stop cortante]

## resultados · 1 · 5 · Resultados · resistencia global

Finalmente, en la resistencia global graficamos la relación entre la demanda y la capacidad de cada piso, que debe ser menor que 1. Todos los modelos cumplen, salvo el MSTA en el primer piso en la dirección X.

[stop resistencia-grafico]
Ahí la relación es 1.030: la suma de resistencias es 146.8 toneladas, menor que la demanda de 151.2, y la hoja de cálculo lo marca como que no cumple y hay que replantear. En cambio, el MCT obtiene una resistencia de 203 toneladas, un 38 % más, porque el metrado automático da una carga de gravedad más representativa y la losa redistribuye las cargas. Quiere decir que, con el mismo edificio, el diagnóstico depende del modelo.

[stop resistencia-diagnostico]

## conclusiones · 1 · 1 · Índice

Y pasamos al último bloque, las conclusiones: qué aporta el trabajo y qué queda abierto.

[stop entrada-conclusiones]

## conclusiones · 1 · 2 · Conclusiones · objetivos

Retomando los objetivos específicos: primero, identificamos que la extracción de resultados, la clasificación de muros y la transcripción a plantillas son actividades críticas y automatizables. Segundo, desarrollamos el marco con sus procesos, diagramas de flujo y trazabilidad para la densidad, el esfuerzo axial, la fisuración, la resistencia al corte y las derivas. Tercero, aplicamos el marco en Alba, que se conecta con ETABS mediante su API, ejecuta las verificaciones y entrega diagnósticos y reportes automáticos. Y cuarto, en el caso evaluado el modelo completo permitió extraer y organizar fuerzas y deformaciones, y vimos que la idealización cambia los resultados y los diagnósticos. Con lo cual la hipótesis se sostiene para el caso estudiado: el marco integrado a ETABS por su API sistematiza la extracción, el procesamiento, la verificación y la documentación. Cabe aclarar que no medimos una reducción de tiempo ni de errores.

[stop objetivos-cumplidos]

## conclusiones · 1 · 3 · Conclusiones · hallazgos

En cuanto a lo que muestra el caso: primero, el modelo completo es menos conservador y más detallado, porque las áreas reparten mejor la carga de la losa y consideran el aporte de los muros ortogonales. Segundo, la E.030 vigente es más exigente que la del 2003, por la combinación direccional de 100 % más 30 % y por factores sísmicos mayores. Tercero, las columnas de 0.25 metros de la propuesta de la E.070 reducen las derivas hasta en 22.61 %, lo que compensa esa mayor exigencia. Y cuarto, Alba queda como una herramienta de apoyo que es software libre. Pero en todos los casos, el criterio del ingeniero sigue siendo el factor determinante.

[stop hallazgos]

## conclusiones · 1 · 4 · Conclusiones · recomendaciones

Finalmente, la investigación deja siete líneas para continuar. En el modelamiento: usar modelos completos con elementos área, estudiar las fuerzas en las uniones en T y en L, y hacer análisis no lineal con macromodelos. En Alba: incorporar el diseño de los confinamientos y mantener este software libre actualizado con el Reglamento Nacional de Edificaciones. Y como nuevos usos: aplicar redes neuronales convolucionales para detectar irregularidades en planta, y usar Alba como recurso docente.

[stop recomendaciones]

## conclusiones · 1 · 5 · Cierre

Con esto terminamos nuestra sustentación. Muchas gracias por su atención; quedamos atentos a las preguntas y observaciones del jurado.

[stop preguntas]
