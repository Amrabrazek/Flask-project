from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'F6A182A6F35BCF2773624CDA7FDAF'

from flask_react import routes