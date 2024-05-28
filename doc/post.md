# Post-analysis
--------------

## Correciones sobre **pre.md**
- Aplicamos la estandarización del zscore de forma "manual", debido a que realizar el procedimiento con el transformer de julearn tardaba demasiado tiempo
y configurar una pipeline completa para unicamente aplicar el zscore resulta innecesario. (En el paper no figuraba que este paso se hacia con julearn, simplemente pensamos que sería más rápido y sencillo de lo que en realidad es).
- No queda claro en **pre.md**, pero FSL *randomise* se utiliza para realizar la t-test, y luego se utliza *cluster* y *atlasquery* para analizar y reportar los resultados de *randomise*.
- Tampoco queda claro que la comparación utilizando el cociente de lateralidad también es en alta dimensión, puesto que consideramos la imágen completa.
- El paper aclara que el atlas utilizado para `atlasquery` es el **Harvard-Oxford**. Esto no figura en **pre.md**.
- Tambien aclara que se utiliza el mapa LQ promedio para comparar los distintos modelos.

## Resultados
El proyecto completo puede ser recreado (una vez instalados los requerimientos) ejecutando [run_project.sh](../src/run_project.sh).

#### Preprocesado
Realizamos el preprocesado utilizando [preprocesado.sh](../src/preprocesado.sh). Este script instala los datasets con datalad, descarga únicamente las imágenes necesarias, y las preprocesa con [preprocess_brain_images.py](../src/preprocess_brain_images.py), que divide los hemisferios y estandariza las nuevas imágenes.

Demostración

#### Cociente de lateralidad
Calculamos el LQ para cada dataset con [laterality_quotient_matrices.py](../src/laterality_quotient_matrices.py). Luego, utilizamos []

#### UMAP

#### LASSO y Boruta

#### Figuras y estadísticas

#### Sexo y mano hábil




## Conclusión