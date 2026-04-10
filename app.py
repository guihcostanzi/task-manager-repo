import os
import threading
import time

from flask import Flask, request, jsonify
from api_test import rodar_testes
from config import get_db_url
from models import db, Usuario, Categoria, Tarefa

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_url()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# --- CRUD USUARIO ---
@app.route('/usuarios', methods=['GET', 'POST'])
@app.route('/usuarios/<int:id>', methods=['PUT', 'DELETE'])
def gerenciar_usuarios(id=None):
    if request.method == 'POST':
        data = request.json
        novo = Usuario(nome=data['nome'], email=data['email'], senha=data['senha'])
        db.session.add(novo)
        db.session.commit()
        return jsonify({"id": novo.id}), 201

    if request.method == 'PUT':
        u = Usuario.query.get_or_404(id)
        data = request.json
        # Atualiza apenas os campos enviados no JSON
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

    # GET (Listar todos)
    usuarios = Usuario.query.all()
    return jsonify([{"id": u.id, "nome": u.nome, "email": u.email} for u in usuarios])

# --- CRUD CATEGORIA ---
@app.route('/categorias', methods=['GET', 'POST'])
@app.route('/categorias/<int:id>', methods=['PUT', 'DELETE'])
def gerenciar_categorias(id=None):
    if request.method == 'POST':
        data = request.json
        nova = Categoria(nome=data['nome'], id_usuario=data['id_usuario'])
        db.session.add(nova)
        db.session.commit()
        return jsonify({"id": nova.id}), 201

    if request.method == 'PUT':
        cat = Categoria.query.get_or_404(id)
        cat.nome = request.json.get('nome', cat.nome)
        db.session.commit()
        return jsonify({"msg": "Atualizado"})

    if request.method == 'DELETE':
        cat = Categoria.query.get_or_404(id)
        db.session.delete(cat)
        db.session.commit()
        return jsonify({"msg": "Removido"})

    categorias = Categoria.query.all()
    return jsonify([{"id": c.id, "nome": c.nome, "id_usuario": c.id_usuario} for c in categorias])

# --- CRUD TAREFA ---
@app.route('/tarefas', methods=['GET', 'POST'])
@app.route('/tarefas/<int:id>', methods=['PUT', 'DELETE'])
def gerenciar_tarefas(id=None):
    if request.method == 'POST':
        data = request.json
        nova = Tarefa(
            descricao=data['descricao'],
            id_usuario=data['id_usuario'],
            id_categoria=data.get('id_categoria')
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
        db.session.commit()
        return jsonify({"msg": "Tarefa atualizada"})

    if request.method == 'DELETE':
        t = Tarefa.query.get_or_404(id)
        db.session.delete(t)
        db.session.commit()
        return jsonify({"msg": "Tarefa removida"})

    # Listagem com filtro opcional por usuário
    user_id = request.args.get('id_usuario')
    query = Tarefa.query
    if user_id:
        query = query.filter_by(id_usuario=user_id)
    
    tarefas = query.all()
    return jsonify([{
        "id": t.id, 
        "descricao": t.descricao, 
        "concluida": t.concluida,
        "id_categoria": t.id_categoria
    } for t in tarefas])

def executar_testes_apos_startup():
        # Espera 4 segundos para garantir que o Flask já está aceitando requisições
        time.sleep(4)
        print("\n[START] Servidor online! Iniciando testes automáticos...\n")
        try:
            rodar_testes()
        except Exception as e:
            print(f"❌ Erro ao rodar testes automáticos: {e}")

if __name__ == '__main__':

    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        thread_testes = threading.Thread(target=executar_testes_apos_startup, daemon=True)
        thread_testes.start()
        
    app.run(debug=True)