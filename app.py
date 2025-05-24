import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from models import db, Livro

load_dotenv()

app= Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv ('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db.init_app(app)


with app.app_context():
    db.create_all()

@app.route("/livros", methods=['GET'])
def listar_livros():
    livros= Livro.query.all()
    return jsonify([{'id': livro.id, 'titulo': livro.titulo, 'autor': livro.autor, 'ano': livro.ano} for livro in livros])

@app.route("/livros", methods=["POST"])
def adicionar_livros():
    data=request.get_json()
    novo=Livro(titulo=data['titulo'], autor=data['autor'], ano=data.get('ano'),)
    db.session.add(novo)
    db.session.commit()
    return jsonify({'mensagem': 'livro adicionado com sucesso'}), 201

@app.route("/livros/<int:id>", methods=["PUT"])
def atualizar_livros(id):
    id_certo= int(id)
    data=request.get_json()
    livro=Livro.query.all(id_certo)
    if not livro:
        return jsonify({'erro': 'livro nao encontrado'}), 404
    livro.titulo = data['titulo']
    livro.autor = data ['autor']
    livro.ano = data.get('ano')
    db.session.commit()
    return jsonify({'mensagem': 'Livro atualizado com sucesso'})

@app.route("/livros/<int:id>", methods=['DELETE'])
def deletar_livro(id):
    id_certo= int(id)
    livro= Livro.query.all(id_certo)
    if not livro:
        return jsonify({'erro': 'Livro nao encontrado'}), 404
    db.session.delete()
    db.session.commit()
    return jsonify({'Mensagem': 'livro deletado'})
