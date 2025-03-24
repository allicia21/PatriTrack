from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api

db = SQLAlchemy()
api = Api(
    version='1.0',
    title='API de Patrimônio',
    description='API para gerenciar o cadastro de patrimônios, categorias e manutenções.',
    doc='/swagger'
)
