#!/usr/bin/env python
import csv
import validacion
import preparaCsv
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap
# from flask_moment import Moment
from flask_script import Manager
from forms import LoginForm, RegistrarForm, ClienteForm, ProductForm

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
# moment = Moment(app)

# Validacion y preparación del archivo de ventas
doc_csv = 'infoventas.csv'
validacion.validar(doc_csv)
registrosventas = preparaCsv.genera_clase(doc_csv)

app.config['SECRET_KEY'] = 'un string que funcione como llave'


# Enrutador del template index.html - Volver a pantalla inicio cuando el usuario no se ha logueado
@app.route('/')
def index_():
    return render_template('index.html', fecha_actual=datetime.utcnow())

# Manejadores de errores
@app.errorhandler(404)
def no_encontrado(e):
    return render_template('404.html'), 404

# Manejadores de errores
@app.errorhandler(500)
def error_interno(e):
    return render_template('500.html'), 500


# Enrutador del template ingresar.html - Validar credenciales e ingresar al sistema
@app.route('/ingresar', methods=['GET', 'POST'])
def ingresar():
    formulario = LoginForm()
    if formulario.validate_on_submit():
        with open('usuarios') as archivo:
            archivo_csv = csv.reader(archivo)
            registro = next(archivo_csv)
            while registro:
                if formulario.usuario.data == registro[0] and formulario.password.data == registro[1]:
                    flash('Bienvenido')
                    session['username'] = formulario.usuario.data
                    mostrarUlt = 5
                    listaUltVentas = []
                    listaUltVentas=listadoVentas(registrosventas, mostrarUlt)
                    return render_template('ultVentas.html',listaUltVentas=listaUltVentas)
                registro = next(archivo_csv, None)
            else:
                flash('Nombre de usuario y/o contraseña incorrecta')
                return redirect(url_for('ingresar'))
    return render_template('login.html', formulario=formulario)

# Enrutador del template registrar.html - Registrar nuevos usuarios en el sistema
@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    formulario = RegistrarForm()
    if formulario.validate_on_submit():
        if formulario.password.data == formulario.password_check.data:
            with open('usuarios', 'a+') as archivo:
                archivo_csv = csv.writer(archivo)
                registro = [formulario.usuario.data, formulario.password.data]
                archivo_csv.writerow(registro)
            flash('Usuario creado correctamente')
            return redirect(url_for('ingresar'))
        else:
            flash('Las passwords no coinciden')
    return render_template('registrar.html', form=formulario)


@app.route('/secret', methods=['GET'])
def secreto():
    if 'username' in session:
        return render_template('private.html', username=session['username'])
    else:
        return render_template('sin_permiso.html')


# Enrutador del template salir.html - Cerrar sesion y salir del sistema
@app.route('/salir', methods=['GET'])
def salir():
    if 'username' in session:
        session.pop('username')
        return render_template('salir.html')
    else:
        return redirect(url_for('index'))


# Enrutador del template index.html - Volver a pantalla inicio cuando el usuario esta logueado
@app.route('/index', methods=['GET'])
def indexAmpliado():
    if 'username' in session:
        return render_template('indexAmpliado.html')
    else:
        return redirect(url_for('index'))


# Enrutador del template ultVentas.html - Mostrar listado de las últimas ventas realizadas
@app.route('/ultVentas', methods=['GET', 'POST'])
def ultVentas():
    if 'username' in session:   
        mostrarUlt = 5
        listaUltVentas = []
        listaUltVentas = listadoVentas(registrosventas, mostrarUlt)
        return render_template('ultVentas.html',listaUltVentas=listaUltVentas)
    else:
        flash('Para acceder debe estar logueado.')
        return redirect(url_for('ingresar'))

# Enrutador del template prodClientes.html - Productos buscados por Clientes
@app.route('/prodClientes', methods=['GET', 'POST'])
def prodClientes():
    if 'username' in session:
        formulario = ClienteForm()
        if formulario.validate_on_submit():
            cliente = formulario.cliente.data.upper()
            if len(cliente) < 3:
                flash('Debe ingresar al menos 3 caracteres para realizar la búsqueda.')
                return render_template('prodClientes.html', form = formulario)
            else:
                listaClientes = buscarClientes(registrosventas,cliente)#llama a funcion para validar si existen los clientes
                if len(listaClientes) == 0:
                    flash('No existen clientes con el nombre ingresado')
                elif len(listaClientes) == 1:
                    listaProductos = listadoProClientes(registrosventas,cliente)
                    return render_template('prodClientes.html', form = formulario, listaProductos = listaProductos, cliente= formulario.cliente.data.upper())
                else:
                    flash('Se encontró mas de un cliente, por favor seleccione el que desea consultar.')
                    return render_template('prodClientes.html', form = formulario, clientes = listaClientes)
        return render_template('prodClientes.html', form = formulario)
    else:
        flash('Para poder ingresar debe estar logueado.')
        return redirect(url_for('ingresar'))

# Enrutador del template prodClientes.html - Productos buscados por Clientes
# (Selección cuando el resultado es mayor a 1)
@app.route('/prodClientes/<clientes>', methods=['GET', 'POST'])
def prodClientes2(clientes):
    if 'username' in session:
        formulario = ClienteForm()
        if formulario.validate_on_submit():
            cliente = formulario.cliente.data.upper()
            if len(cliente) < 3:
                flash('Debe ingresar al menos 3 caracteres para realizar la búsqueda.')
                return redirect(url_for('prodClientes'))
            else:
                listaclientes = buscarClientes(registrosventas,cliente)
                if len(listaclientes) == 0:
                    flash('No existen clientes con el nombre ingresado.')
                    return redirect(url_for('prodClientes'))                   
                elif len(listaclientes) == 1:
                    listaProductos = listadoProClientes(registrosventas,cliente)
                    return render_template('prodClientes.html', form = formulario, listaProductos = listaProductos, cliente= formulario.cliente.data.upper())
                else:
                    flash('Se encontró mas de un cliente, por favor seleccione el que desea consultar.')
                    return render_template('prodClientes.html', form = formulario, clientes = listaclientes)
        else:
            cliente = clientes
            listaclientes = buscarClientes(registrosventas,cliente)
            listaProductos = listadoProClientes(registrosventas,cliente)
            return render_template('prodClientes.html', form = formulario, listaProductos = listaProductos, cliente= cliente)
    else:
        flash('Para poder acceder debe estar logueado.')
        return redirect(url_for('ingresar'))

# Enrutador del template cliProductos.html - Clientes buscados por productos
@app.route('/cliProductos', methods=['GET', 'POST'])
def cliProductos():
    if 'username' in session:
        formulario = ProductForm()
        if formulario.validate_on_submit():
            producto = formulario.producto.data.upper()
            if len(producto) < 3:
                flash('Debe ingresar al menos 3 caracteres para realizar la búsqueda.')
                return render_template('cliProductos.html', form=formulario)
            else:
                listaProductos = buscarProductos(registrosventas, producto)
                if len(listaProductos) == 0:
                    flash('No existen productos con la descripción ingresada.')
                elif len(listaProductos) == 1:
                    listaClientes = listadoCliProductos(registrosventas,producto)
                    return render_template('cliProductos.html', form = formulario, listaClientes = listaClientes, producto= formulario.producto.data.upper())
                else:
                    flash('Se encontró mas de un producto, por favor seleccione el que desea consultar.')
                    return render_template('cliProductos.html', form = formulario, productos = listaProductos)
        return render_template('cliProductos.html', form=formulario)
    else:
        flash('Para poder acceder debe estar logueado.')
        return redirect(url_for('ingresar'))

# Enrutador del template cliProductos.html - Clientes buscados por productos
# (selección cuando el resultado es mayor que 1)
@app.route('/cliProductos/<productos>', methods=['GET', 'POST'])
def cliProductos2(productos):
    if 'username' in session:
        formulario = ProductForm()
        if formulario.validate_on_submit():
            producto = formulario.producto.data.upper()
            if len(producto) < 3:
                flash('Debe ingresar al menos 3 caracteres para realizar la búsqueda.')
                return redirect(url_for('cliProductos'))
            else:
                listaProductos = buscarProductos(registrosventas,producto)
                if len(listaProductos) == 0:
                    flash('No existen productos con la descripción ingresada.')
                    return redirect(url_for('cliProductos'))                   
                elif len(listaProductos) == 1:
                    listaClientes = listadoCliProductos(registrosventas,producto)
                    return render_template('cliProductos.html', form = formulario, listaClientes = listaClientes, producto= formulario.producto.data.upper())
                else:
                    flash('Se encontró mas de un producto, por favor seleccione el que desea consultar.')
                    return render_template('cliProductos.html', form = formulario, productos = listaProductos)
        else:
            producto = productos
            listaProductos = buscarProductos(registrosventas,producto)
            listaClientes = listadoCliProductos(registrosventas,producto)
            return render_template('cliProductos.html', form = formulario, listaClientes = listaClientes, producto = producto)
    else:
        flash('Para poder acceder debe estar logueado.')
        return redirect(url_for('ingresar'))

# Listado de productos con mayor volúmen de ventas
@app.route('/masVendidos', methods=['GET', 'POST'])
def masVendidos():
    if 'username' in session:
        listaMasVendidos = []
        cantidad = 5
        listaMasVendidos = encontrarMasVendidos(registrosventas = registrosventas, cantidad=cantidad)
        return render_template('masVendidos.html', listaMasVendidos = listaMasVendidos)
    else:
        flash('Para poder acceder debe estar logueado.')
        return redirect(url_for('ingresar'))


# Clientes que más gastaron dinero haciendo compras
@app.route('/masGastaron', methods=['GET', 'POST'])
def masGastaron():
    if 'username' in session:
        listaMasGastaron = []
        cantidad = 5
        listaMasGastaron = mas_gastaron(registrosventas = registrosventas, cantidad=cantidad)
        return render_template('masGastaron.html', listaMasGastaron = listaMasGastaron)
    else:
        flash('Para poder acceder debe estar logueado.')
        return redirect(url_for('ingresar'))

# Se define función para buscar el listado de las últimas ventas realizadas
def listadoVentas(registrosventas, ultimos):
    listaVentas = []
    registrosventas_reverse = registrosventas.reverse()
    while ultimos > len(registrosventas):
        ultimos -= 1
    for x in range(ultimos):
        listaVentas.append(registrosventas[x])
    registrosventas_reverse = registrosventas.reverse()
    return listaVentas


# Se define función para buscar clientes a partir del nombre ingresado por el usuario
def buscarClientes(registrosventas, nomCliente):
    listaCliente = []
    for x in range(len(registrosventas)):
        if nomCliente in registrosventas[x].cliente:
            if registrosventas[x].cliente in listaCliente:
                pass
            else:
                listaCliente.append(registrosventas[x].cliente)
        else:
            pass
    return listaCliente

# Se define función para buscar el listado de productos comprados por un cliente
def listadoProClientes(registrosventas, cliente):
    nomCliente = cliente.upper()
    listaProductos = []
    for x in range(len(registrosventas)):
        if nomCliente in registrosventas[x].cliente:
            listaProductos.append(registrosventas[x])
    return listaProductos


# Se define función para buscar productos a partir de la descripción ingresada por el usuario
def buscarProductos(registrosventas, nomProducto):
    listaProducto = []
    for x in range(len(registrosventas)):
        if nomProducto in registrosventas[x].producto:
            if registrosventas[x].producto in listaProducto:
                pass
            else:
                listaProducto.append(registrosventas[x].producto)
        else:
            pass
    return listaProducto

# Se define función para buscar el listado de clientes que compraron un producto
def listadoCliProductos(registrosventas, producto):
    nomProducto = producto.upper()
    listaclientes = []
    for x in range(len(registrosventas)):
        if nomProducto in registrosventas[x].producto:
            listaclientes.append(registrosventas[x])
    return listaclientes

# Se define función para hallar los productos con mayor volúmen de ventas
def encontrarMasVendidos(registrosventas, cantidad):
    listaProducto = []
    listaCantProducto = []
    posProducto=0

    for posRegistro in range(len(registrosventas)):
        if posRegistro == 0:
            listaProducto.append(registrosventas[posRegistro].producto)
            listaCantProducto.append([])
            listaCantProducto[posProducto]= [registrosventas[posRegistro],0]
        else:
            if registrosventas[posRegistro].producto in listaProducto:
                pass
            else:
                posProducto = posProducto + 1
                listaProducto.append(registrosventas[posRegistro].producto)
                listaCantProducto.append([])
                listaCantProducto[posProducto]= [registrosventas[posRegistro],0]

    for x in range(len(listaProducto)):
        for y in range(len(registrosventas)):
            if listaProducto[x] in registrosventas[y].producto:
                listaCantProducto[x][1]= listaCantProducto[x][1] + registrosventas[y].cantidad
            else:
                pass

    listaCantProducto.sort(key=lambda listaCantProducto: listaCantProducto[1], reverse=True)

    while cantidad > len(listaProducto):
        cantidad -= 1
    list_cant = []
    for x in range(cantidad):
        list_cant.append([0]*2)
        list_cant[x][0] = listaCantProducto[x][0]
        list_cant[x][1] = listaCantProducto[x][1]
    return list_cant


# Se define función para hallar los clientes que más gastaron dinero haciendo compras
def mas_gastaron(registrosventas, cantidad):
    clientes = []
    cant_cliente = []
    columna=0

    for x in range(len(registrosventas)):
        if x == 0:
            clientes.append(registrosventas[x].cliente)
            cant_cliente.append([])
            cant_cliente[columna]=[0, registrosventas[x]]
        else:
            if registrosventas[x].cliente in clientes:
                pass
            else:
                clientes.append(registrosventas[x].cliente)
                columna = columna + 1
                cant_cliente.append([])
                cant_cliente[columna]=[0, registrosventas[x]]


    for x in range(len(clientes)):
        for y in range(len(registrosventas)):
            if clientes[x] in registrosventas[y].cliente:
                cant_cliente[x][0]= cant_cliente[x][0] + (registrosventas[y].cantidad * registrosventas[y].precio)
            else:
                pass

    cant_cliente.sort(reverse=True)

    while cantidad > len(clientes):
        cantidad -= 1
    list_cant = []
    for x in range(cantidad):
        list_cant.append([0]*2)
        list_cant[x][0] = cant_cliente[x][0]
        list_cant[x][1] = cant_cliente[x][1]
    return list_cant





if __name__ == "__main__":
    # app.run(host='0.0.0.0', debug=True)
    manager.run()
