--------------------------------------------
FLUJO GENERAL DEL PROGRAMA

Inicialmente se realizan las validaciones solicitadas sobre el archivo de ventas, a través del archivo validacion.py

Luego de pasar satisfactoriamente las validaciones, se emplea la clase Csv creada en el archivo preparaCsv, para ordenar los campos del archivo de ventas y almacenar los valores de los mismos en mayúscula, de forma que queden preparados para su uso en el resto de las funciones del programa.

Luego se cargan los templates correspondientes a cada opción del menú seleccionada por el usuario, donde a su vez se emplean los formularios definidos en el archivo forms.py para el ingreso de datos por parte de los usuarios (login, registro de usuario, busqueda de clientes por productos y viceversa) y finalmente, cada template lleva a cabo la ejecución de diversas funciones que se encuentran definidas en el archivo app.py, y que permiten realizar las consultas requeridas para la posterior visualización de la información de acuerdo a la opción seleccionada.

--------------------------------------------
ESTRUCTURA UTILIZADA PARA REPRESENTAR LA INFORMACIÓN DEL ARCHIVO

Se definió una clase que posee como atributos los 5 campos del archivo de ventas, cuyos valores se asignan siempre en mayuscula luego de que son ordenados.

--------------------------------------------
COMO SE USA EL PROGRAMA

Para ejecutar el programa se accede desde la línea de comandos, se ubica la ruta donde se encuentra la carpeta que contiene los archivos del programa, y se ejecuta el comando "pipenv run python app.py runserver" obteniendo la dirección del sitio web la cual se ingresa en el navegador para visualizar la pantalla de inicio.

El aplicativo consta de una pantalla inicial con las opciones de menú: Inicio, Ingresar y Registrarse

Inicio: muestra un mensaje de bienvenida.
Ingresar: solicita usuario y contraseña para acceder al aplicativo.
Registrarse: permite el registro de un nuevo usuario.

Una vez que se ingresa con con un usuario válido desde la opción Ingresar, se presenta un menu ampliado con las siguientes opciones:

Últimas ventas: muestra el listado de las últimas 5 ventas registradas.
Productos por Cliente: permite consultar los productos comprados por un cliente, a partir del ingreso de su nombre.
Clientes por producto: permite consultar los clientes que compraron un determinado producto, a partir del ingreso de la descripción del producto.
Productos más vendidos: muestra el listado de los 5 productos con mayor cantidad de ventas.
Clientes que más compraron: muestra el listado de los 5 clientes con mayores montos de compras.
Salir: cierra sesion y sale del sistema.

--------------------------------------------
CLASES:


Se crearon clases para los formularios de ingresos de datos en el archivo forms.py, a partir de clases que se importan de FlaskForm:
LoginForm
RegistrarForm
ClienteForm
ProductForm 


Se creo una clase denominada Csv dentro del archivo preparaCsv.py que se encarga de ordenar los campos del archivo de ventas y almacenar los valores de los mismos en mayúscula.


En el archivo validacion.py se crearon 2 clases, destinadas al manejo de errores durante el proceso de validación de datos.



--------------------------------------------
FUNCIONES:

Dentro del archivo app.py se encuentran la mayoria de las funciones definidas, y para cada una se indica un breve comentario de la función que desempeña.
