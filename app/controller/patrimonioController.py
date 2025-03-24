##from flask import Blueprint, request, jsonify
##from app.models.patrimonio import Patrimonio

# Criando um blueprint para o controlador de patrimônio
##patrimonio_bp = Blueprint('patrimonio_bp', __name__)

# Rota para listar todos os patrimônios
##@patrimonio_bp.route('/', methods=['GET'])
##def listar_patrimonios():
    ##patrimonio_lista = Patrimonio.query.all()
    ##return jsonify([patrimonio.to_dict() for patrimonio in patrimonio_lista])

# Rota para cadastrar um novo patrimônio
##@patrimonio_bp.route('/CadastrarPatrimonio', methods=['POST'])
##def cadastrar_patrimonio():
   ## data = request.get_json()
   ## novo_patrimonio = Patrimonio(nome=data['nome'], descricao=data['descricao'], 
                               ##  categoria=data['categoria'], situacao=data['situacao'],
                                 ##  data_aquisicao=data['data_aquisicao'])

    
    ##db.session.add(novo_patrimonio)
   ## db.session.commit()
   ## return jsonify(novo_patrimonio.to_dict()), 201

from flask import Blueprint, request, jsonify
from app.app import db
from app.models.patrimonio import Patrimonio
from app.schemas.patrimonioSchema import ProdutoViewSchema, ErrorSchema
from datetime import datetime

# Criando um blueprint para o controlador de patrimônio
patrimonio_bp = Blueprint('patrimonio_bp', __name__)

# Rota para listar todos os patrimônios
@patrimonio_bp.route('/', methods=['GET'])
def listar_patrimonios():
    patrimonio_lista = Patrimonio.query.all()
    
    # Converte os objetos de patrimônio para dicionários
    resposta = [patrimonio.to_dict() for patrimonio in patrimonio_lista]

    # Validar a resposta com o schema de ProdutoViewSchema
    erro = ProdutoViewSchema.validar_resposta(resposta)
    if erro:
        # Retorna erro de validação com status 404
        return jsonify(ErrorSchema.format_error(erro)), 404
    
    # Retorna os dados com status 200
    return jsonify(resposta), 200

# Rota para cadastrar um novo patrimônio
@patrimonio_bp.route('/CadastrarPatrimonio', methods=['POST'])
def cadastrar_patrimonio():
    data = request.get_json()

    # Criar o novo patrimônio a partir dos dados recebidos
    novo_patrimonio = Patrimonio(
        nome=data['nome'],
        descricao=data.get('descricao', ''),
        categoria=data.get('categoria', ''),
        situacao=data.get('situacao', ''),
        data_aquisicao=datetime.strptime(data['data_aquisicao'], "%Y-%m-%d")
    )

    # Converter o patrimônio para dicionário
    resposta = novo_patrimonio.to_dict()

    # Validar a resposta com o schema de ProdutoViewSchema
    erro = ProdutoViewSchema.validar_resposta(resposta)
    if erro:
        # Retorna erro de validação com status 404
        return jsonify(ErrorSchema.format_error(erro)), 404


    # Adicionar e salvar no banco de dados
    db.session.add(novo_patrimonio)
    db.session.commit()
    
    # Retorna os dados com status 201 (criado)
    return jsonify(resposta), 201

