# Pre-analysis
--------------

## Introducción
Elegimos reproducir el paper: [Is it left or is it right? A classification approach for investigating hemispheric differences in low and high dimensionality](https://link.springer.com/article/10.1007/s00429-021-02418-1).

Algunas de las razones para elegir el paper fueron:
- Al ser realizado por el mismo instituto donde trabaja el profesor, y dónde se desarrollaron las herramientas presentadas en el curso, tenemos la oportunidad de aplicarlas de forma más directa, particularmente porque fueron utilizadas en el paper mencionado.
- Los datos ya fueron pre-procesados (salvo una parte específica al paper), lo que nos permite concentrarnos directamente en la implementación.
- La idea del paper es interesante, y a simple vista consideramos que provee un nivel de dificultad adecuado para poder ser reproducido siguiendo el procedimiento detallado en el texto.

La hipótesis (nuestra) es que siguiendo los pasos denotados en el paper, llegaremos a las mismas conclusiones.

La hipótesis presentada en el paper es que el procedimiento presentado permite hallar características que permiten diferenciar entre ambos hemisferios del cerebro.


## Métodos
Se utilizan los datasets de [AOMIC](https://nilab-uva.github.io/AOMIC.github.io/), [PIOP1](https://openneuro.org/datasets/ds002785/versions/2.0.0) Y [PIOP2](https://openneuro.org/datasets/ds002790/versions/2.0.0).

La adquisición de los datos, su pre-procesado y mucho más está aclarado en la siguiente página: https://www.nature.com/articles/s41597-021-00870-6 .

Una herramienta ampliamente utilizada por el paper es [FSL](https://fsl.fmrib.ox.ac.uk/fsl/docs/#/), la cual también utilizaremos para poder reproducirlo apropiadamente.

Para un pre-procesamiento de los datos se sigue el procedimiento 

El procesado de los datos, incluyendo los features, los modelos a utilizar, y su evaluación, está "dividido" en tres métodos diferentes:
1. Comparación univariada.
2. Clasificación en baja dimensión.
3. Clasificación en alta dimensión.

La comparación univariada calcula un "coeficiente de lateralidad" (notado LQ) para cada voxel, que luego es analizado a través de pruebas t, utilizando "threshold-free cluster enhancement" (conq FSL), para hallar posibles asimetrías significativas (en el sentido del p-value).

La clasificación en baja dimensión consta de reducir las dimensiones de los hemisferios utilizando UMAP, (nosotros utilizaremos [esta versión](https://umap-learn.readthedocs.io/en/latest/index.html)). Luego, se pasa la versión de baja dimensionalidad a una SVM, que clasifica los hemisferios en izquierdo y derecho.

La clasificación en alta dimensión utiliza los voxels de forma directa, que son procesados por un algoritmo [LASSO](https://en.wikipedia.org/wiki/Lasso_(statistics)). La salida de este proceso es una vez más analizada por el algoritmo de Boruta (algoritmo de [feature selection](https://en.wikipedia.org/wiki/Feature_selection)), para reducir el impacto de la multicolinearidad, y poder elegir apropiadamente las features "relevantes".

Posteriormente, se comparan los tres procedimientos a través del [coeficiente de similaridad de Dice](https://en.wikipedia.org/wiki/Dice-S%C3%B8rensen_coefficient).

Finalmente, se realiza un análisis de clasificación de hemisferios con estos tres procedimientos según sexo y mano hábil, por separado.

### Procedimiento detallado
De antemano, aclaramos que en el caso de cualquier parámetro/hiperparámetro que no figure explícitamente en el paper, utilizaremos siempre los valores por defecto, aclarando la versión del software utilizado (en el post.md). Para casos donde tampoco se menciona la versión del software utilizado, utilizaremos la última versión disponible, también aclarándolo debidamente.

- Adquirimos las imagenes de cada sujeto, en la carpeta `derivatives/vbm/sub-nnnn/`. El archivo que buscamos tiene el formato: `sub-nnnn_desc-VBM_GMvolume.nii.gz`. Este archivo ya fue pre-procesado por AOMIC.
- Realizamos el pre-procesamiento notado en el paper: dividimos ambos hemisferios segun la linea central, rotamos el hemisferio izquierdo sobre el eje X para alinear ambos hemisferios, y estandarizamos (Z-score) los valores de los voxels.
La parte de dividir los hemisferios y alinearlos lo implementamos con un script. La parte del z-score, la implementamos con el preprocessing de julearn, utilizando el transformer `zscore`.
Esto se realiza para prevenir que los clasificadores únicamente utilicen la diferencia hemisférico promedio para identificar los hemisferios.
- Ya tenemos los datos. Ahora, queremos realizar los tres tipos de análisis previamente mencionados.    
- Utilizamos python3.8, y la librería scikit-learn.
Los hemisferios se leen como matrices 3D utilizando 'nilearn'. Las matrices se transforman a vectores de una dimensión de longitud V, donde V = número de voxels.
Los vectores resultantes de dimensión 1xV se concatenan para crear una matriz de datos de NxV, con N = cantidad de hemisferios = cantidad de sujetos en el dataset * 2.
En el dataset1, N = 432, mientras que en el dataset2, N = 452.

- Para la comparación univariada, creamos un cociente de lateralidad (LQ) para cada voxel, sustrayendo el valor del voxel del hemisferio izquierdo al voxel correspondiente del hemisferio derecho, y luego dividiendo por la suma total de los valores VBM de ambos hemisferios. Las imagenes LQ resultantes se concatenan para formar una "imagen" 4D por dataset, que contiene información de todos los sujetos.
- Para determinar la significancia de las asimetrías, utilizamos una one-sample t-test, con 0 como referencia, aplicando TFCE, con FSL randomise con 5000 permutaciones. Para esto, utilizamos el algoritmo cluster de FSL, combinado con el comando "atlas query", como figura en el paper.
Se reportan los resultados con p value < 0.05.

- Para la clasificación en baja dimensión, primero, utilizamos UMAP (la librería de python, linkeada previamente). Debido a que no se mencionan hiperparámetros más allá de que reducimos a dos dimensiones (que de igual forma es lo predeterminado), utilizamos todas las opciones 'default' del programa.
- Una vez aplicado UMAP, utilizamos una SVM, a través del modelo `svm` de julearn, con `problem_type=classification`. Realizmos cross validation con los valores por defecto de julearn, que son 5 folds y 5 repeticiones (con la función `run_cross_validation()`).

- Para la clasificación en alta dimensión, utilizamos LASSO (`sklearn.linear_model.Lasso`). Como se nota en el paper, utilizamos cross-validation con los parámetros por defecto de threefold y una repetición. Cada voxel es un feature de entrada. Como ya se mencionó, además, utilizamos el algoritmo Boruta de selección de features, a través del algoritmo cluster de FSL (ya fue aclarado al inicio, pero al no tener parámetros específicos utilizamos todo por defecto), combinado con el comando "atlas query".
- Los resultados del algoritmo de Boruta se redimensionan de 1D a 3D para poder visualizarlos utilizando [SurfIce](https://www.nitrc.org/projects/surfice/). 

- Para comparar resultados con la t-test y el algoritmo de Boruta, se computa el DSC entre los mapas "izquierdos" (LQ negativo) y "derechos" (LQ positivo) de asimetría, considerando distintos thresholds, comenzando desde 0.2, con incrementos de 0.2, hasta 6, para los valores positivos, y lo mismo pero con todos los signos invertidos (de -0.2 a -6, con -0.2 de incremento) para el caso negativo.

- Para realizar las pruebas de clasificación de hemisferios según sexo y mano hábil, evaluamos los modelos derivados en pasos anteriores, y comparamos su efectividad (entre los tres modelos derivados) utilizando DSC.

- Para realizar los gráficos, utlizamos una combinación de seaborn y matplotlib. Los parámetros son todos estándar, salvo aquellos como el título, o el nombre de los ejes, para poder asimilarse lo más posible a las figuras presentadas en el paper. No replicaremos la figura 1 puesto que únicamente representa cómo es el pre-procesado, y no se recrea a partir de datos.

- La primer figura a realizar contiene un KDEplot (Kernel Density Estimation) y un Scatterplot (ploteados con `seaborn.kdeplot` y `seaborn.scatterplot`) sobre los datos en bajas dimensiones (es decir, aquellos sobre los que aplicamos UMAP). Realizamos el gráfico para ambos datasets, destacando la pertenencia de los datos a un hemisferio o al otro.

- La segunda figura involucra los datos en altas dimensiones y es un poco más compleja. Utilizamos [nilearn](https://nilearn.github.io/dev/index.html), especificamente la función `plot_surf_stat_map` para realizar un gráfico de las superficies 3D representadas por los voxels que se obtienen de procesar las imágenes con los modelos de altas dimensiones. Se muestran tres "modelos" o cómputos: el LQ (con los valores en un rango [-0.2, -.1]), los p-values obetenidos las T-test (en un rango de [0.05, 0.01]), y la clasificación resultante del algortimo de Boruta, indicando para cada voxel si es relevante o no.
Esto se realiza para ambos datasets (notar que cuando hablamos de datasets, siempre aplicamos estos modelos en base a la imágen promedio del dataset, luego de haber entrenado los modelos con todo el dataset. Esto no se menciona específicamente en ninguna parte pero nos pareció el procedimiento más adecuado).

- Además, se incluyen gráficos de comparación entre los tres modelos, calculando el DSC en comparación a el LQ, variando los thresholds. Para ello, convertimos las imágenes en vectores 1D, y luego convertimos los datos en booleanos (en base al threshold en el caso de LQ y en base a si el p-value es < 0.05 en el caso de t-test, Boruta ya es booleano), para finalmente calcular el DSC utilizando `scipy.spatial.distance.dice`, de la librería [scipy](https://docs.scipy.org/doc/scipy/index.html). Los gráficos se realizan por separado para cada dataset, y se realiza un gráfico por cada "tipo" de threshold de LQ (positivo implica que el threshold es "rightward" o "hacia la derecha", y viceversa). Para esto, utlizamos `seaborn.barplot`.

- La tercer figura a replicar involucra la evaluación de los modelos según sexo y mano hábil. Realizamos el mismo procedimiento para ambos datasets. La primer parte de la figura involucra un KDE con un scatter plot integrado en base al modelo de baja dimensión, que nos muestra cómo el modelo clasificó a cada una de las imágenes (hemisferios izquierdo o hemisferio derecho). Tenemos cuatro gráficos por dataset: hombre vs mujer, y derecho vs zurdo. El método para realizar los gráficos es prácticamente idéntico al mencionado anteriormente (utilizamos `seaborn.kdeplot` y `seaborn.scatterplot`). Además, se agrega un valor de "precisión", que representa el promedio de la precisión del SVM cross validado al identificar los hemisferios.
- Luego, tenemos una superficie 3D representando los voxels significantes elegidos por el algoritmo de Boruta (nuevamente, consideramos la imágen promedio). Se muestran los voxeles elegidos por el algoritmo, clasificándolos según si pertenecen al grupo A (i.e. hombre o derecho), al grupo B (mujer o zurdo), o a ambos. Además, se muestra el DSC entre ambos grupos. Debido a que no hay ninguna especificación, consideramos que al igual que en la figura anterior, se considera únicamente el hemisferio derecho. Nuevamente tenemos cuatro figuras por dataset (hombres vs mujeres, del frente y de atrás, y lo mismo para derechos y zurdos).
- Además, se calcula la precisión de la clasificación voxel-based utilizando el clasificador LASSO para cada subsample (es decir, cada participante), y se toma el promedio. Realizamos este cálculo de igual forma que en el caso anterior que usamos LASSO, pero ahora para cada subsample.