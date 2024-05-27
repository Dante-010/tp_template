# Post-analysis
--------------

## Correciones sobre **pre.md**
Aplicamos la estandarización del zscore de forma "manual", debido a que realizar el procedimiento con el transformer de julearn tardaba demasiado tiempo
y configurar una pipeline completa para unicamente aplicar el zscore resulta innecesario. (En el paper no figuraba que este paso se hacia con julearn, simplemente pensamos que sería más rápido y sencillo de lo que en realidad es).

## Resultados
#### Laterality Quotient
Comando: `randomise -i data_matrix.nii.gz -o output -d design.txt -1 -T -n 5000 -x -C 2.3 --cluster --cluster-localthresh --cluster-connectivity --atlasquery`

```
    -i: Especifica el archivo de matriz de datos de entrada.
    -o: Especifica el prefijo para los archivos de salida.
    -d: Especifica el archivo de matriz de diseño.
    -1: Realiza una prueba t de una muestra.
    -T: Especifica el uso de TFCE (Enhancement de Clúster sin Umbral) para la corrección de múltiples comparaciones.
    -n: Especifica el número de permutaciones para realizar.
    -x: Especifica el uso de una matriz de diseño 2D.
    -C: Especifica el umbral para formar clústeres.
    --cluster: Habilita el umbral de clústeres.
    --cluster-localthresh: Habilita el umbral local para los clústeres.
    --cluster-connectivity: Habilita la conectividad de clústeres.
    --atlasquery: Habilita la consulta del atlas para etiquetar clústeres significativos.
```    


## Conclusión