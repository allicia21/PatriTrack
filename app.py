from flask_openapi3 import OpenAPI, Info, Tag
from flask import jsonify, redirect, request
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from models._init_ import Session, Patrimonio
from flask_cors import CORS

from schemas.Patrimonio import ListagemPatrimoniosSchema, PatrimonioAtualizaSchema, PatrimonioBuscaSchema, PatrimonioBuscaSchemaDelete, PatrimonioDelSchema, PatrimonioSchema, PatrimonioViewSchema, apresenta_patrimonio, apresenta_patrimonios
from schemas.erro import ErrorSchema

import logging

logging.basicConfig(level=logging.INFO)

info = Info(title="API para Gerencimento de Patrimonios", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
patrimonio_tag = Tag(name="Patrimonio", description="Adição, visualização e remoção de patriminio à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""

    return redirect('/openapi')


@app.post('/cadastrarPatrimonio', tags=[patrimonio_tag],
          responses={"200": PatrimonioViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_patrimonio(form: PatrimonioSchema):
    """Adiciona um novo Patrimonio à base de dados."""

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

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Patrimonio de mesmo nome já salvo na base."
        return {"mesage": error_msg}, 409
    
    if not patrimonio:
        return {"message": "Não foi possível salvar novo item."}, 400
         
    # efetivando a inserção
    session.commit()

    return apresenta_patrimonio(patrimonio), 200             


@app.get('/buscarPatrimonios', tags=[patrimonio_tag],
         responses={"200": ListagemPatrimoniosSchema, "404": ErrorSchema})
def get_patrimonios():
    """Faz a busca por todos os patrimonios cadastrados na base de dados."""

    # criando conexão com a base
    session = Session()
    # fazendo a busca
    patrimonios = session.query(Patrimonio).all()

    if not patrimonios:
        # se não há patrimonios cadastrados
        return {"patrimonios": []}, 200
    else:
        # retorna a representação de produto
        print(patrimonios)
        return apresenta_patrimonios(patrimonios), 200


@app.get('/patrimonioById', tags=[patrimonio_tag],
         responses={"200": PatrimonioViewSchema, "404": ErrorSchema})
def get_produto(query: PatrimonioBuscaSchema):
    """Faz a busca por um Patrimonio a partir do id do patrimonio."""

    patrimonio_id = query.id
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    patrimonio = session.query(Patrimonio).filter(Patrimonio.id == patrimonio_id).first()

    if not patrimonio:
        # se o patrimonio não for encontrado
        error_msg = "patrimonio não encontrado."
        return {"mesage": error_msg}, 404
    else:
        # retorna a representação de um patrimonio
        return apresenta_patrimonio(patrimonio), 200


@app.delete('/deletePatrimonio', tags=[patrimonio_tag],
            responses={"200": PatrimonioDelSchema, "404": ErrorSchema})
def del_patrimonio(query: PatrimonioBuscaSchemaDelete):
    """Deleta um Patrimonio a partir do nome informado"""

    patrimonio_nome = unquote(unquote(query.nome))
    print(patrimonio_nome)
    # criando conexão com a base
    session = Session()

    patrimonio = session.query(Patrimonio).filter(Patrimonio.nome == query.nome).first()

    if not patrimonio:
        return {"message": "Patrimônio não encontrado."}, 404
    
    print(patrimonio.nome)

    session.delete(patrimonio) 

    # efetivando a remoção
    session.commit()

    return {"message": "Patrimônio deletado com sucesso."}, 200


@app.put('/atualizarPatrimonio', tags=[patrimonio_tag],
         responses={"200": PatrimonioViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def update_situacao(form: PatrimonioAtualizaSchema):
    """Atualiza a situação de um patrimônio na base de dados."""

    try:
        # Criando conexão com a base
        session = Session()

        # Buscando o patrimônio pelo ID
        patrimonio = session.query(Patrimonio).filter(Patrimonio.id == form.id).first()

        # Verificando se o patrimônio foi encontrado
        if not patrimonio:
            return {"message": "Patrimônio não encontrado."}, 404

        # Atualizando a situação do patrimônio
        patrimonio.situacao = form.situacao

        # Salvando as alterações
        session.commit()

        # Retornando a representação atualizada do patrimônio
        return apresenta_patrimonio(patrimonio), 200
    
    except Exception as e:
        # Capturando o erro e logando a exceção completa
        logging.error(f"Erro ao atualizar a situação do patrimônio: {str(e)}")

        # Caso algum erro aconteça
        error_msg = "Não foi possível atualizar a situação do patrimônio."
        return {"message": error_msg, "error": str(e)}, 400

