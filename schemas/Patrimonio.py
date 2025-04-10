from pydantic import BaseModel
from typing import List
from models.Patrimonio import Patrimonio


class PatrimonioSchema(BaseModel):
    """ Define como um novo patrimonio ou ativo a ser inserido, deve ser representado."""

    nome: str = ""
    descricao: str = ""
    categoria: int = 3
    situacao: str = ""
    data_aquisicao: str = ""


class PatrimonioBuscaSchemaDelete(BaseModel):
    """ Define como deve ser a estrutura que representa a busca com o nome do patrimonio. """
    nome: str = "notebook"

class PatrimonioBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca feita pelo id do patrimonio. """
    id: int = 1

class PatrimonioAtualizaSchema(BaseModel):

    id: int = 1
    situacao: str = ""

class ListagemPatrimoniosSchema(BaseModel):
    """ Define como uma listagem de patrimonios será retornada.
    """
    patrimonios:List[PatrimonioSchema]


def apresenta_patrimonios(patrimonios: List[Patrimonio]):
    """ Retorna uma representação do patrimonio seguindo o schema definido em
        PatrimonioViewSchema.
    """
    result = []
    for Patrimonio in patrimonios:
        result.append({
            "nome": Patrimonio.nome,
            "descricao": Patrimonio.descricao,
            "categoria": Patrimonio.categoria,
            "situacao": Patrimonio.situacao,
            "data_aquisicao": Patrimonio.data_aquisicao
        })

    return {"patrimonios": result}


class PatrimonioViewSchema(BaseModel):
    """ Define como um patrimonio será retornado: patrimonios.
    """
    id: int = 1
    nome: str 
    descricao: str 
    categoria: int 
    situacao: str 
    data_aquisicao: str = "2025-04-10"

class PatrimonioDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_patrimonio(patrimonio: Patrimonio):
    """ Retorna uma representação do patrimonio seguindo o schema definido em
        PatrimonioViewSchema.
    """
    return {
        "id": patrimonio.id,
        "nome": patrimonio.nome,
        "descricao": patrimonio.descricao,
        "categoria": patrimonio.categoria,
        "situacao": patrimonio.situacao,
        "data_aquisicao": patrimonio.data_aquisicao
    }
