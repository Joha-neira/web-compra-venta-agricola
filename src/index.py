from flask import Flask, render_template, request, redirect, url_for, flash
from conexionbd import getConn, cx_Oracle
app = Flask(__name__)


#inicializar sesión
app.secret_key = 'mysecretkey'

#inicializar user
global user
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

@app.route('/editar-usuario')
def editarUsuario():
    global user
    if len(user)==0:
        return render_template('/inicio-sesion.html')
    else:
        return render_template('/editar-usuario.html', user=user)

@app.route('/editar-productor')
def editarProductor():
    global user
    if len(user)==0:
        return render_template('/inicio-sesion.html')
    else:
        return render_template('/editar-productor.html', user=user)

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

@app.route('/perfil-productor-editado', methods=['GET','POST'])
def perfilProductorEditado():
    if request.method == 'POST':
        username=request.form['username']
        nombreempresa=request.form['nombreempresa']
        rutempresa=request.form['rutempresa']
        razonsocial=request.form['razonsocial']
        telefono1=request.form['telefono1']
        telefono2=request.form['telefono2']
        direccion=request.form['direccion']
        global user
        correo=user[0][0]
        conn=getConn()
        crs = conn.cursor()
        sql = """update productor set username=:username, nombreempresa=:nombreempresa, rutempresa=:rutempresa, razonsocial=:razonsocial, telefono1=:telefono1, telefono2=:telefono2, direccion=:direccion where correo=:correo"""
        crs.execute(sql,[username,nombreempresa,rutempresa,razonsocial,telefono1,telefono2,direccion,correo])
        conn.commit()
        sql = """select correo, pass, nvl(username,' '), nombre, apellido, nombreempresa, razonsocial, nvl(rutempresa,' '), nvl(telefono1,' '), tipologin, nvl(telefono2,' '), nvl(direccion,' ') from productor where correo=:correo"""
        crs.execute(sql,[correo])
        user=crs.fetchall()
        return render_template('/perfil-productor.html', user=user)
    if request.method == 'GET':
        if len(user)==0:
            return render_template('/inicio-sesion.html')
        else:
            return render_template('/perfil-productor.html', user=user)

#ruta perfil de usuario
@app.route('/perfil-usuario', methods=['GET','POST'])
def perfilUsuario():
    if request.method == 'POST':
        correo=request.form['correo']
        passw=request.form['password']
        conn=getConn()
        crs = conn.cursor()
        sql = """select correo, password, nvl(username,' '), nombre, apellido, nvl(rutusuario,' '), nvl(telefono1,' '), nvl(telefono2,' '), nvl(domicilio,' '), tipologin from usuario where correo=:correo"""
        crs.execute(sql,[correo])
        global user
        user=crs.fetchall()
        print(user)
        if correo == "" or passw == "" :
            user = []
            return render_template('/inicio-sesion.html')
        else:
            if len(user)>0:
                if correo == user[0][0] and passw == user[0][1]:
                    return render_template('/perfil-usuario.html', user=user)
                else: 
                    user= []
                    return render_template('/inicio-sesion.html')
            else:
                sql = """select correo, pass, nvl(username,' '), nombre, apellido, nombreempresa, razonsocial, nvl(rutempresa,' '), nvl(telefono1,' '), tipologin, nvl(telefono2,' '), nvl(direccion,' ') from productor where correo=:correo"""
                crs.execute(sql,[correo])
                user=crs.fetchall()
                if len(user)>0:
                    if correo == user[0][0] and passw == user[0][1]:
                        return render_template('/perfil-productor.html', user=user)
                    else:   
                        user= []
                        return render_template('/inicio-sesion.html')
                else:
                    user= []
                    return render_template('/inicio-sesion.html')
    if request.method == 'GET':
        if len(user)==0:
            return render_template('/inicio-sesion.html')
        else:
            if user[0][9]=="c":
                return render_template('/perfil-usuario.html', user=user)
            else:
                return render_template('/perfil-productor.html', user=user)

#ruta vista lista de productos
@app.route('/productos')
def productos():
    conn=getConn()
    crs= conn.cursor()
    global user
    correo = user[0][0]
    sql = "SELECT * FROM producto where correoproductor = :correo"
    crs.execute(sql,[correo])
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
        global user
        correo = user[0][0]
        conn=getConn()
        crs = conn.cursor()
        sql = """INSERT INTO producto (idProducto,nombreProducto,cantidad,precio,categoria,correoproductor)
                VALUES (:idProducto,:nombreProducto,:cantidad,:precio,:categoria, :correoproductor)"""
        crs.execute(sql,[idProducto,nombreProducto,cantidad,precio,str(categoria),correo])
        conn.commit()
        conn.close()
        flash('Producto agregado satisfactoriamente')
    return redirect(url_for('productos'))

# #ruta para eliminar producto
# @app.route('/eliminar-producto/<string:id>')
# def eliminarProducto(id):
#     return

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
    global user
    if len(user)>0:
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
    else:
        return render_template('/inicio-sesion.html')

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
    return render_template('/inicio-sesion.html')

#ruta de contactos
@app.route('/contactos')
def contactos():
    return render_template('contactos.html')   

#ruta de valoraciones
@app.route('/valoraciones')
def valoraciones():
    return render_template('valoraciones.html')


#ruta de vista-producto
@app.route('/vista-producto', methods=['POST'])
def vistaProducto(): 
    if request.method=='POST':
        nombrebusqueda=request.form['busqueda']
        conn=getConn()
        crs = conn.cursor()
        sql = """select * from producto where lower(nombreproducto) like lower('%'||:nombre||'%')"""
        crs.execute(sql,[nombrebusqueda])
        data=crs.fetchall()
    return render_template('/vista-producto.html',productos=data)  


@app.route('/editar-producto/<idproducto>', methods=['GET','POST'])
def editarProducto(idproducto):
    conn=getConn()
    crs = conn.cursor()
    sql = """select idproducto, nombreproducto, cantidad, precio, categoria from producto where idproducto=:idproducto"""
    crs.execute(sql,[idproducto])
    producto=crs.fetchall()
    return render_template('editar-producto.html',producto=producto)
    
@app.route('/producto-editado', methods=['GET','POST'])
def productoEditado():
    if request.method == 'POST':
        idproducto=request.form['idproducto']
        nombreproducto=request.form['nombreproducto']
        cantidad=request.form['cantidad']
        precio=request.form['precio']
        categoria=request.form['categoria']
        conn=getConn()
        crs = conn.cursor()
        sql = """update producto set nombreproducto=:nombreproducto, cantidad=:cantidad, precio=:precio, categoria=:categoria where idproducto=:idproducto"""
        crs.execute(sql,[nombreproducto,cantidad,precio,categoria,idproducto])
        conn.commit()
        sql = """select idproducto, nombreproducto, cantidad, precio, categoria from producto """
        crs.execute(sql,[])
        productos=crs.fetchall()
        return render_template('/productos.html', productos=productos)
    if request.method == 'GET':
        return render_template('/perfil-productor.html')
     

if __name__ == "__main__":
    app.run(debug=True)