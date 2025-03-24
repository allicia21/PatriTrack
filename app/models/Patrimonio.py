from app.app import db

class Patrimonio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200), nullable=True)
    categoria = db.Column(db.Integer)
    situacao = db.Column(db.String(200), nullable=True)
    data_aquisicao = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f'<Patrimonio {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'categoria': self.categoria,
            'situacao': self.situacao,
            'data_aquisicao': self.data
        }
