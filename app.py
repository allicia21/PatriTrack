from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from models._init_ import Session, Patrimonio
from flask_cors import CORS

from schemas.Patrimonio import ListagemPatrimoniosSchema, PatrimonioBuscaSchema, PatrimonioDelSchema, PatrimonioSchema, PatrimonioViewSchema, apresenta_patrimonio, apresenta_patrimonios
from schemas.erro import ErrorSchema

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
patrimonio_tag = Tag(name="Patrimonio", description="Adição, visualização e remoção de patriminio à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/patrimonio', tags=[patrimonio_tag],
          responses={"200": PatrimonioViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_patrimonio(form: PatrimonioSchema):
    """Adiciona um novo Patrimonio à base de dados

    Retorna uma representação dos patrimonios.
    """
    patrimonio = Patrimonio(
        nome=form.nome,
        descricao=form.descricao,
        categoria=form.categoria,
        situacao=form.situacao)
    try:
        # criando conexão com a base
        session = Session()
        # adicionando patrimonio
        session.add(patrimonio)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        return apresenta_patrimonio(patrimonio), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Patrimonio de mesmo nome já salvo na base :/"
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        return {"mesage": error_msg}, 400                   


@app.get('/buscarPatrimonios', tags=[patrimonio_tag],
         responses={"200": ListagemPatrimoniosSchema, "404": ErrorSchema})
def get_patrimonios():
    """Faz a busca por todos os patrimonios cadastrados

    Retorna uma representação da listagem de patrimonios.
    """
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    patrimonios = session.query(Patrimonio).all()

    if not patrimonios:
        # se não há produtos cadastrados
        return {"produtos": []}, 200
    else:
        # retorna a representação de produto
        print(patrimonios)
        return apresenta_patrimonios(patrimonios), 200


@app.get('/patrimonioById', tags=[patrimonio_tag],
         responses={"200": PatrimonioViewSchema, "404": ErrorSchema})
def get_produto(query: PatrimonioBuscaSchema):
    """Faz a busca por um Patrimonio a partir do id do patrimonio

    Retorna uma representação dos patrimonios.
    """
    patrimonio_nome = query.nome
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    patrimonio = session.query(Patrimonio).filter(Patrimonio.nome == patrimonio_nome).first()

    if not patrimonio:
        # se o patrimonio não for encontrado
        error_msg = "patrimonio não encontrado na base :/"
        return {"mesage": error_msg}, 404
    else:
        # retorna a representação de produto
        return apresenta_patrimonio(patrimonio), 200


@app.delete('/DeletePatrimonio', tags=[patrimonio_tag],
            responses={"200": PatrimonioDelSchema, "404": ErrorSchema})
def del_patrimonio(query: PatrimonioBuscaSchema):
    """Deleta um Patrimonio a partir do nome de um patrimonio informado

    Retorna uma mensagem de confirmação da remoção.
    """
    patrimonio_nome = unquote(unquote(query.nome))
    print(patrimonio_nome)
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Patrimonio).filter(Patrimonio.nome == patrimonio_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        return {"mesage": "Patrimonio removido", "id": patrimonio_nome}, 200
    else:
        # se o produto não foi encontrado
        error_msg = "Patrimonio não encontrado na base :/"
        return {"mesage": error_msg}, 404
