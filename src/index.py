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
    if request.method == 'GET':
        if len(user)==0:
            return render_template('/inicio-sesion.html')
        else:
            if user[0][9]=="c":
                return render_template('/perfil-usuario.html', user=user)
            else:
                return render_template('/perfil-productor.html', user=user)

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