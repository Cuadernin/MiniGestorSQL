# Interfaz gráfica que realiza operaciones básicas en SQL
GUI que permite realizar distintas operaciones en SQL usando python.

<figure class="half" style="display:flex">
    <img style="width:400px" src="https://github.com/Cuadernin/MiniGestorSQL/blob/master/images/imagen2.png">
    <img style="width:600px" src="https://github.com/Cuadernin/MiniGestorSQL/blob/master/images/imagen3.png">
    <figcaption></figcaption>
</figure>

## Informacion 👌
  Permite realizar distintas operaciones a una base de datos en MYSQL. Puede modificarse para ser aplicado a una base de datos en PostgreSQL y SQLlite3.
  | Operación | Descripción |
| ------ | ------ |
| Crear base de datos| Crea base de datos ingresando el nombre |
| Crear tabla | Desde la configuración default o con una sentencia SQL |
| Insertar registros  | Con sentencia SQL |
| Eliminar registros | Con sentencia SQL |
| Consultas | Todos los registros o consulta personalizada |

## Modificaciones 📋
 El código, como cualquier otro, puede modificarse a gusto de cada usuario. No obstante, para su funcionamiento debe **modificarse** la siguiente linea:
 <p align="center">
 <img src="https://github.com/Cuadernin/MiniGestorSQL/blob/master/images/codigo.png" height="200" width="500">
 </p>
 
 Dicha linea se encuentra en otras partes del  codigo.
 
 
 ### Nota 📪
 La funcion `Importar datos` de la pestaña archivo se encuentra deshabilitada. Para habilitarla debe escribir el código que _rellene la tabla seleccionada_. El GUI selecciona la base y la tabla además de leer el csv, entonces únicamente debe agregar la parte faltante. Puede encontrar algunos ejemplos en las siguientes ligas:
  -  [dataquest](https://www.dataquest.io/blog/loading-data-into-postgres/)
  -  [plainenglish](https://py.plainenglish.io/how-to-import-a-csv-file-into-a-mysql-database-using-python-script-791b051c5c33) ---> *Forma óptima de hacerlo*

 
 
 

