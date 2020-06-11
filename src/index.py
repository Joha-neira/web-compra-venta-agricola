from flask import Flask, render_template

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