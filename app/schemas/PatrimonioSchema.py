from pydantic import BaseModel
from typing import List
from app.models.Patrimonio import Patrimonio


class PatrimonioSchema(BaseModel):
    """ Define como um novo produto a ser inserido deve ser representado
    """
    nome: str = "Notebook"
    descricao: str = "Notebook Dell para Analista"
    categoria: int = 2
    situacao: str = "Em uso"
    data_aquisicao: str = "2021-01-01"


class PatrimonioBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do produto.
    """
    nome: str = "Teste"


class ListagemPatrimoniosSchema(BaseModel):
    """ Define como uma listagem de produtos será retornada.
    """
    Patrimonio:List[PatrimonioSchema]


class PatrimonioViewSchema(BaseModel):
    """ Define como um produto será retornado: produto + comentários.
    """
    nome: str = "Notebook"
    descricao: str = "Notebook Dell para Analista"
    categoria: int = 2
    situacao: str = "Em uso"
    data_aquisicao: str = "2021-01-01"

class PatrimonioDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_patrimonio(patrimonio: Patrimonio):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    return {
        "id": patrimonio.id,
        "nome": patrimonio.nome,
        "descricao": patrimonio.descricao,
        "categoria": patrimonio.categoria,
        "situacao": patrimonio.situacao,
        "data_aquisicao": patrimonio.data_aquisicao}
