from flask import Flask, render_template

app = Flask(__name__)

#ruta del home
@app.route('/')
def home():
    return render_template('index.html')

#ruta del registro de cliente
@app.route('/registro-cliente')
def registroCliente():
    return render_template('registro-cliente.html')

#ruta del registro de productor
@app.route('/registro-productor')
def registroProductor():
    return render_template('registro-productor.html')

if __name__ == "__main__":
    app.run(debug=True)