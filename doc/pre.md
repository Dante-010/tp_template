# Pre-analysis
--------------

## Introducción
Elegimos reproducir el paper: [Is it left or is it right? A classification approach for investigating hemispheric differences in low and high dimensionality](https://link.springer.com/article/10.1007/s00429-021-02418-1).

Algunas de las razones para elegir el paper fueron:
- Al ser realizado por el mismo instituto donde trabaja el profesor, y dónde se desarrollaron las herramientas presentadas en el curso, tenemos la oportunidad de aplicarlas de forma más directa, particularmente porque fueron utilizadas en el paper mencionado.
- Los datos ya fueron pre-procesados, lo que nos permite concentrarnos directamente en la implementación.
- La idea del paper es interesante, y a simple vista consideramos que provee un nivel de dificultad adecuado para poder ser reproducido siguiendo el procedimiento detallado en el texto.

La hipótesis (nuestra) es que siguiendo los pasos denotados en el paper, llegaremos a las mismas conclusiones.

La hipótesis presentada en el paper es que el procedimiento presentado permite hallar características que permiten diferenciar entre ambos hemisferios del cerebro.


## Métodos
Se utilizan los datasets de [AOMIC](https://nilab-uva.github.io/AOMIC.github.io/), [PIOP1](https://openneuro.org/datasets/ds002785/versions/2.0.0) Y [PIOP2](https://openneuro.org/datasets/ds002790/versions/2.0.0).

La adquisición de los datos, su pre-procesado y mucho más está aclarado en la siguiente página: https://www.nature.com/articles/s41597-021-00870-6 .

Una herramienta ampliamente utilizada por el paper es [FSL](https://fsl.fmrib.ox.ac.uk/fsl/docs/#/), la cual también utilizaremos para poder reproducirlo apropiadamente.

El procesado de los datos, incluyendo los features, los modelos a utilizar, y su evaluación, está "dividido" en tres métodos diferentes:
1. Comparación univariada.
2. Clasificación en baja dimensión.
3. Clasificación en alta dimensión.

La comparación univariada calcula un "coeficiente de lateralidad" (notado LQ) para cada voxel, que luego es analizado a través de pruebas t, utilizando "threshold-free cluster enhancement" (con FSL), para hallar posibles asimetrías significativas (en el sentido del p-value).

La clasificación en baja dimensión consta de reducir las dimensiones de los hemisferios utilizando UMAP, (nosotros utilizaremos [esta versión](https://umap-learn.readthedocs.io/en/latest/index.html)). Luego, se pasa la versión de baja dimensionalidad a una SVM, que clasifica los hemisferios en izquierdo y derecho.

La clasificación en alta dimensión utiliza los voxels de forma directa, que son procesados por un algoritmo [LASSO](https://en.wikipedia.org/wiki/Lasso_(statistics)). La salida de este proceso es una vez más analizada por el algoritmo de Boruta (algoritmo de [feature selection](https://en.wikipedia.org/wiki/Feature_selection)), para reducir el impacto de la multicolinearidad, y poder elegir apropiadamente las features "relevantes".

Posteriormente, se comparan los tres procedimientos a través del [coeficiente de similaridad de Dice](https://en.wikipedia.org/wiki/Dice-S%C3%B8rensen_coefficient).

Finalmente, se realiza un análisis de clasificación de hemisferios con estos tres procedimientos según sexo y mano hábil, por separado.