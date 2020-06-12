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

if __name__ == "__main__":
    app.run(debug=True)