from flask import Flask, render_template, request, redirect, url_for, flash
from conexionbd import getConn, cx_Oracle
app = Flask(__name__)

#inicializar sesión
app.secret_key = 'mysecretkey'
#inicializar user
user = []

#ruta del home
@app.route('/')
def home():
    conn=getConn()
    crs= conn.cursor()
    sql = "SELECT * FROM producto"
    crs.execute(sql)
    data = crs.fetchall()
    return render_template('/index.html', productos = data)
#ruta inicio de sesion
@app.route('/inicio-sesion')
def iniciosesion():
    return render_template('/inicio-sesion.html')

correo_usuario : str
#ruta perfil de usuario
@app.route('/perfil-usuario', methods=['GET','POST'])
def perfilUsuario():
    if request.method == 'POST':
        correo=request.form['correo']
        global correo_usuario
        correo_usuario = correo
        conn=getConn()
        crs = conn.cursor()
        sql = """select * from usuario where correo=:correo"""
        crs.execute(sql,[correo])
        user=crs.fetchall()
        return render_template('/perfil-usuario.html', user=user)
    else: 
        return render_template('/perfil-usuario.html', correo_usuario)
    

#ruta vista lista de productos
@app.route('/productos')
def productos():
    conn=getConn()
    crs= conn.cursor()
    sql = "SELECT * FROM producto"
    crs.execute(sql)
    data = crs.fetchall()
    return render_template('/productos.html', productos = data)

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
        flash('Producto agregado satisfactoriamente')
    return redirect(url_for('productos'))

#ruta para eliminar producto
@app.route('/eliminar-producto/<string:id>')
def eliminarProducto(id):
    return


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
    conn=getConn()
    crs = conn.cursor()
    global correo_usuario
    sql = """select p.nombreproducto, c.cantidad, p.categoria, (p.precio*c.cantidad) from carrito c join producto p on (p.idproducto = c.idproducto) where correo = :correo"""
    crs.execute(sql,[correo_usuario])
    data = crs.fetchall()
    totalCarrito=0
    for producto in data:
        totalCarrito += producto[3]
    conn.close()
    return render_template('carrito.html',productos = data, totalCarrito = totalCarrito) 

#ruta agregar al carrito
@app.route('/agregar-carrito/<id><cant>')   
def agregarCarrito(id,cant):
    # conn=getConn()
    # crs= conn.cursor()
    # sql = """select * from producto where idproducto = :id"""
    # crs.execute(sql,[id])
    # data = crs.fetchall()
    cantidad = cant
    idproducto = id
    global correo_usuario
    correo = correo_usuario
    print(cantidad, idproducto, correo)
    conn=getConn()
    crs = conn.cursor()
    sql = """INSERT INTO carrito (cantidad, idproducto, correo)
            VALUES (:cantidad,:idproducto,:correo)"""
    crs.execute(sql,[cantidad,idproducto,correo])
    conn.commit()
    sql = """select p.nombreproducto, c.cantidad, p.categoria, (p.precio*c.cantidad) from carrito c join producto p on (p.idproducto = c.idproducto) where correo = :correo"""
    crs.execute(sql,[correo_usuario])
    data = crs.fetchall()
    conn.close()
    return render_template('carrito.html',productos = data)

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