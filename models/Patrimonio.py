from sqlalchemy import Column, String, Integer, DateTime, Float
from datetime import datetime
from typing import Union
from  models.base import Base


class Patrimonio(Base):
    __tablename__ = 'patrimonio'

    id = Column("pk_produto", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    descricao = Column(String(200))
    categoria = Column(Integer)
    situacao = Column(String(200))
    data_aquisicao = Column(DateTime, default=datetime.now())


    def __init__(self, nome:str, descricao:str, categoria:int, situacao:str,
                 data_aquisicao:Union[DateTime, None] = None):
    
        self.nome = nome
        self.descricao = descricao
        self.categoria = categoria
        self.situacao = situacao

        # se não for informada, será o data exata da inserção no banco
        if data_aquisicao:
            self.data_aquisicao = data_aquisicao

    def __repr__(self):
        return f"<Patrimonio {self.nome}>"
