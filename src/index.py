from flask import Flask, render_template, request, redirect, url_for
from conexionbd import getConn, cx_Oracle

app = Flask(__name__)

#ruta del home
@app.route('/')
def home():
    return render_template('index.html')

#ruta inicio de sesion
@app.route('/inicio-sesion')
def iniciosesion():
    return render_template('/inicio-sesion.html')

#ruta perfil de usuario
@app.route('/perfil-usuario')
def perfilUsuario():
    return render_template('/perfil-usuario.html')

@app.route('/productos')
def productos():
    return render_template('/productos.html')

#ruta del registro de cliente
@app.route('/registro-cliente')
def registroCliente():
    return render_template('registro-cliente.html')

#ruta del agregar cliente
@app.route('/agregar-cliente', methods=['POST'])
def addCliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos  = request.form['apellidos']
        email  = request.form['email']
        contrasena = request.form['contrasena']
        conn=getConn()
        crs = conn.cursor()
        sql = """INSERT INTO usuario (correo,password,nombre,apellido)
                VALUES (:correo,:password,:nombre,:apellido)"""
        crs.execute(sql,[email,contrasena,nombre,apellidos])
        conn.commit()
        conn.close()
    return 'received'

#ruta del registro de productor
@app.route('/registro-productor')
def registroProductor():
    return render_template('registro-productor.html')

#ruta del agregar productor
@app.route('/agregar-productor', methods=['POST'])
def addProductor():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos  = request.form['apellidos']
        nombreEmpresa = request.form['nombreEmpresa']
        razonSocial = request.form['razonSocial']
        direccion = request.form['direccion']
        email  = request.form['email']
        contrasena = request.form['contrasena']
        conn=getConn()
        crs = conn.cursor()
        sql = """INSERT INTO productor (correo,pass,nombre,apellido,nombreempresa,razonsocial,direccion)
                VALUES (:correo,:password,:nombre,:apellido,:nombreempresa,:razonsocial,:direccion)"""
        crs.execute(sql,[email,contrasena,nombre,apellidos,nombreEmpresa,razonSocial,direccion])
        conn.commit()
        conn.close()
    return 'received'

#ruta del ingreso de productos
@app.route('/ingreso-productos')
def ingresoProductos():
    return render_template('ingreso-productos.html')    

#ruta para agregar producto
@app.route('/agregar-producto',methods=['POST'])
def addProducto():
    if request.method == 'POST':
        idProducto = request.form['idProducto']
        nombreProducto  = request.form['nombreProducto']
        cantidad = request.form['cantidad']
        precio = request.form['precio']
        categoria = request.form['categoria']
        conn=getConn()
        crs = conn.cursor()
        sql = """INSERT INTO producto (idProducto,nombreProducto,cantidad,precio,categoria)
                VALUES (:idProducto,:nombreProducto,:cantidad,:precio,:categoria)"""
        crs.execute(sql,[idProducto,nombreProducto,cantidad,precio,str(categoria)])
        conn.commit()
        conn.close()
    return 'received'


#ruta de favoritos
@app.route('/favoritos')
def favoritos():
    return render_template('favoritos.html')

#ruta de compras
@app.route('/compras')
def compras():
    return render_template('compras.html')

#ruta de carrito
@app.route('/carrito')
def carrito():
    return render_template('carrito.html')    

#ruta de contactos
@app.route('/contactos')
def contactos():
    return render_template('contactos.html')   

#ruta de valoraciones
@app.route('/valoraciones')
def valoraciones():
    return render_template('valoraciones.html')       


if __name__ == "__main__":
    app.run(debug=True)