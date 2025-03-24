from datetime import date
from sqlite3 import IntegrityError
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request
from app.extensions import db, api  # Importando as extensões
from app.models.Patrimonio import Patrimonio
from app.schemas.PatrimonioSchema import PatrimonioSchema, apresenta_patrimonio
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError

from flask import Flask
from app.extensions import db, api  # Importando as extensões

# Inicializando o app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patrimonio_ativos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializando as extensões
db.init_app(app)
api.init_app(app)

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
patrimonio_tag = Tag(name="Produto", description="Adição, visualização e remoção de produtos à base")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect('/openapi')

@app.post('/patrimonio', tags=[patrimonio_tag], responses={200: {"model": PatrimonioSchema}})
def add_patrimonio(form: PatrimonioSchema):
    from datetime import datetime
    data_aquisicao = datetime.strptime(form.data_aquisicao, "%Y-%m-%d").date()
    """Adiciona um novo Produto à base de dados."""
    patrimonio = Patrimonio(
        nome=form.nome,
        descricao=form.descricao,
        categoria=form.categoria,
        situacao=form.situacao,
        data_aquisicao=form.data_aquisicao)
    
    try:
        session = db.session
        session.add(patrimonio)
        session.commit()
        return apresenta_patrimonio(patrimonio), 200

    except IntegrityError:
        error_msg = "Patrimonio de mesmo nome já salvo na base :/"
        return {"message": error_msg}, 409

    except Exception:
        error_msg = "Não foi possível salvar novo item :/"
        return {"message": error_msg}, 400

@app.post('/patrimonio', tags=[patrimonio_tag])
def get_patrimonio(query: PatrimonioSchema):
    """Faz a busca por um Produto a partir do id do produto."""
    patrimonio_nome = query.nome
    session = Session()
    produto = session.query(Patrimonio).filter(Patrimonio.nome == patrimonio_nome).first()

    if not produto:
        error_msg = "Produto não encontrado na base :/"
        return {"message": error_msg}, 404
    else:
        return apresenta_patrimonio(produto), 200
