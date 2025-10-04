from flask import Flask

# Creamos la aplicación Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Hola 👋, tu aplicación Flask es
