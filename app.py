import os
import threading
import time
from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS

from api_test import rodar_testes
from config import get_db_url
from models import db, Usuario, Categoria, Tarefa

app = Flask(__name__)

# --- CORS ---
CORS(app)

# --- CONFIG ---
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_url()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# =========================
# LOGIN
# =========================
@app.route('/login', methods=['POST'])
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json

    user = Usuario.query.filter_by(email=data['email']).first()

    if user and user.senha == data['senha']:
        return jsonify({
            "id": user.id,
            "nome": user.nome
        }), 200

    return jsonify({"erro": "Login inválido"}), 401


# =========================
# CRUD USUARIOS
# =========================
@app.route('/usuarios', methods=['GET', 'POST'])
@app.route('/usuarios/<int:id>', methods=['PUT', 'DELETE'])
def gerenciar_usuarios(id=None):

    if request.method == 'POST':
        data = request.json

        novo = Usuario(
            nome=data['nome'],
            email=data['email'],
            senha=data['senha']
        )

        db.session.add(novo)
        db.session.commit()

        return jsonify({"id": novo.id}), 201

    if request.method == 'PUT':
        u = Usuario.query.get_or_404(id)
        data = request.json

        u.nome = data.get('nome', u.nome)
        u.email = data.get('email', u.email)

        if 'senha' in data:
            u.senha = data['senha']

        db.session.commit()
        return jsonify({"msg": "Usuário atualizado"})

    if request.method == 'DELETE':
        u = Usuario.query.get_or_404(id)
        db.session.delete(u)
        db.session.commit()
        return jsonify({"msg": "Usuário removido"})

    # GET
    usuarios = Usuario.query.all()

    return jsonify([
        {"id": u.id, "nome": u.nome, "email": u.email}
        for u in usuarios
    ])


# =========================
# CRUD CATEGORIAS
# =========================
@app.route('/categorias', methods=['GET', 'POST'])
@app.route('/categorias/<int:id>', methods=['PUT', 'DELETE'])
def gerenciar_categorias(id=None):

    if request.method == 'POST':
        data = request.json

        nova = Categoria(
            nome=data['nome'],
            id_usuario=data['id_usuario']
        )

        db.session.add(nova)
        db.session.commit()

        return jsonify({"id": nova.id}), 201

    if request.method == 'PUT':
        cat = Categoria.query.get_or_404(id)

        cat.nome = request.json.get('nome', cat.nome)

        db.session.commit()
        return jsonify({"msg": "Categoria atualizada"})

    if request.method == 'DELETE':
        cat = Categoria.query.get_or_404(id)

        db.session.delete(cat)
        db.session.commit()

        return jsonify({"msg": "Categoria removida"})

    # GET
    categorias = Categoria.query.all()

    return jsonify([
        {"id": c.id, "nome": c.nome, "id_usuario": c.id_usuario}
        for c in categorias
    ])


# =========================
# CRUD TAREFAS
# =========================
@app.route('/tarefas', methods=['GET', 'POST'])
@app.route('/tarefas/<int:id>', methods=['PUT', 'DELETE'])
def gerenciar_tarefas(id=None):

    if request.method == 'POST':
        data = request.json

        nova = Tarefa(
            descricao=data['descricao'],
            id_usuario=data['id_usuario'],
            id_categoria=data.get('id_categoria'),
            data_inicio=datetime.fromisoformat(data['data_inicio']) if data.get('data_inicio') else None,
            data_fim=datetime.fromisoformat(data['data_fim']) if data.get('data_fim') else None
        )

        db.session.add(nova)
        db.session.commit()

        return jsonify({"id": nova.id}), 201

    if request.method == 'PUT':
        t = Tarefa.query.get_or_404(id)
        data = request.json

        t.descricao = data.get('descricao', t.descricao)
        t.concluida = data.get('concluida', t.concluida)
        t.id_categoria = data.get('id_categoria', t.id_categoria)

        if 'data_inicio' in data:
            t.data_inicio = datetime.fromisoformat(data['data_inicio']) if data['data_inicio'] else None

        if 'data_fim' in data:
            t.data_fim = datetime.fromisoformat(data['data_fim']) if data['data_fim'] else None

        db.session.commit()
        return jsonify({"msg": "Tarefa atualizada"})

    if request.method == 'DELETE':
        t = Tarefa.query.get_or_404(id)

        db.session.delete(t)
        db.session.commit()

        return jsonify({"msg": "Tarefa removida"})

    # GET com filtro por usuário
    user_id = request.args.get('id_usuario')

    query = Tarefa.query

    if user_id:
        query = query.filter_by(id_usuario=user_id)

    tarefas = query.all()

    return jsonify([{
        "id": t.id,
        "descricao": t.descricao,
        "concluida": t.concluida,
        "id_categoria": t.id_categoria,
        "data_cadastro": t.data_cadastro.isoformat() if t.data_cadastro else None,
        "data_inicio": t.data_inicio.isoformat() if t.data_inicio else None,
        "data_fim": t.data_fim.isoformat() if t.data_fim else None
    } for t in tarefas])

# TESTES AUTOMATICOS
def executar_testes_apos_startup():
    time.sleep(4)
    print("\n[START] Servidor online! Iniciando testes automáticos...\n")
    try:
        rodar_testes()
    except Exception as e:
        print(f"Erro ao rodar testes: {e}")


if __name__ == '__main__':

    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        thread_testes = threading.Thread(
            target=executar_testes_apos_startup,
            daemon=True
        )
        thread_testes.start()

    app.run(debug=False)
