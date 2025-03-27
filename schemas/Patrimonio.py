from pydantic import BaseModel
from typing import List
from models.Patrimonio import Patrimonio


class PatrimonioSchema(BaseModel):
    """ Define como um novo patrimonio ou ativo a ser inserido, deve ser representado."""

    nome: str = "notebook"
    descricao: str = "notebook dell"
    categoria: int = 1
    situacao: str = "novo" 
    data_aquisicao: str = "2021-10-10"


class PatrimonioBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do patrimonio. """
    id: int = 1

class PatrimonioAtualizaSchema(BaseModel):

    id: int = 1
    situacao: str = "insira  a nova situação"

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
    nome: str = "Notebook"
    descricao: str = "notebook dell analista"
    categoria: int = 1
    situacao: str = "novo"
    data_aquisicao: str = "2025-03-25"

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
