from flask import Flask, render_template, request
from conexionbd import getConn, cx_Oracle
app = Flask(__name__)

global user
user = []

#ruta del home
@app.route('/')
def home():
    return render_template('index.html')

#ruta inicio de sesion
@app.route('/inicio-sesion')
def iniciosesion():
    return render_template('/inicio-sesion.html')

@app.route('/editar-usuario')
def editarUsuario():
    global user
    if len(user)==0:
        return render_template('/inicio-sesion.html')
    else:
        return render_template('/editar-usuario.html', user=user)

@app.route('/perfil-usuario-editado', methods=['GET','POST'])
def perfilUsuarioEditado():
    if request.method == 'POST':
        username=request.form['username']
        rutusuario=request.form['rutusuario']
        telefono1=request.form['telefono1']
        telefono2=request.form['telefono2']
        domicilio=request.form['domicilio']
        global user
        correo=user[0][0]
        conn=getConn()
        crs = conn.cursor()
        sql = """update usuario set username=:username, rutusuario=:rutusuario, telefono1=:telefono1, telefono2=:telefono2, domicilio=:domicilio where correo=:correo"""
        crs.execute(sql,[username,rutusuario,telefono1,telefono2,domicilio,correo])
        conn.commit()
        sql = """select correo, password, nvl(username,' '), nombre, apellido, nvl(rutusuario,' '), nvl(telefono1,' '), nvl(telefono2,' '), nvl(domicilio,' ') from usuario where correo=:correo"""
        crs.execute(sql,[correo])
        user=crs.fetchall()
        return render_template('/perfil-usuario.html', user=user)
    if request.method == 'GET':
        if len(user)==0:
            return render_template('/inicio-sesion.html')
        else:
            return render_template('/perfil-usuario.html', user=user)


#ruta perfil de usuario
@app.route('/perfil-usuario', methods=['GET','POST'])
def perfilUsuario():
    if request.method == 'POST':
        correo=request.form['correo']
        passw=request.form['password']
        conn=getConn()
        crs = conn.cursor()
        sql = """select correo, password, nvl(username,' '), nombre, apellido, nvl(rutusuario,' '), nvl(telefono1,' '), nvl(telefono2,' '), nvl(domicilio,' ') from usuario where correo=:correo"""
        crs.execute(sql,[correo])
        global user
        user=crs.fetchall()
        if correo == "" or passw == "" :
            user = []
            return render_template('/inicio-sesion.html')
        else:
            if correo == user[0][0] and passw == user[0][1]:
                return render_template('/perfil-usuario.html', user=user)
            else:
                user= []
                return render_template('/inicio-sesion.html')
    if request.method == 'GET':
        if len(user)==0:
            return render_template('/inicio-sesion.html')
        else:
            return render_template('/perfil-usuario.html', user=user)

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

#ruta del ingreso de productos
@app.route('/ingreso-productos')
def ingresoProductos():
    return render_template('ingreso-productos.html')    

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
    sql = """select p.nombreproducto, c.cantidad, p.categoria, (p.precio*c.cantidad) from carrito c join producto p on (p.idproducto = c.idproducto) where correo = :correo"""
    crs.execute(sql,[user[0][0]])
    data = crs.fetchall()
    totalCarrito=0
    for producto in data:
        totalCarrito += producto[3]
    conn.close()
    return render_template('carrito.html',productos = data, totalCarrito = totalCarrito) 

#ruta agregar al carrito
@app.route('/agregar-carrito/<id>/<cant>')   
def agregarCarrito(id,cant):
    # conn=getConn()
    # crs= conn.cursor()
    # sql = """select * from producto where idproducto = :id"""
    # crs.execute(sql,[id])
    # data = crs.fetchall()
    cantidad = cant
    idproducto = id
    correo = user[0][0]
    print(cantidad, idproducto, correo)
    conn=getConn()
    crs = conn.cursor()
    sql = """INSERT INTO carrito (cantidad, idproducto, correo)
            VALUES (:cantidad,:idproducto,:correo)"""
    crs.execute(sql,[cantidad,idproducto,correo])
    conn.commit()
    sql = """select p.nombreproducto, c.cantidad, p.categoria, (p.precio*c.cantidad) from carrito c join producto p on (p.idproducto = c.idproducto) where correo = :correo"""
    crs.execute(sql,[correo])
    data = crs.fetchall()
    totalCarrito=0
    for producto in data:
        totalCarrito += producto[3]
    conn.close()
    return render_template('carrito.html',productos = data, totalCarrito = totalCarrito)

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