from flask import Flask


app = Flask(__name__)


# Aqui você pode importar as rotas
from app import routes
