from flask import Flask, render_template

app = Flask(__name__)

#ruta del home
@app.route('/')
def home():
    return render_template('index.html')

#inicio de sesion
@app.route('/inicio-sesion')
def iniciosesion():
    return render_template('/inicio-sesion.html')

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

if __name__ == "__main__":
    app.run(debug=True)