import requests
import time
import sys

BASE_URL = "http://127.0.0.1:5000"

def imprimir_log(acao, status, detalhes=""):
    cor = "\033[92m" if status == "SUCESSO" else "\033[91m"
    reset = "\033[0m"
    print(f"{cor}[{status}] {acao}{reset} {detalhes}")

def rodar_testes():
    print("="*50)
    print("INICIANDO TESTES DE API (CRUD COMPLETO)")
    print("="*50)

    # Variáveis para armazenar os IDs gerados
    user_id = None
    cat_id = None
    tarefa_id = None

    try:
        # ---------------------------------------------------------
        # 1. INCLUSÃO (POST)
        # ---------------------------------------------------------
        print("\n--- ETAPA 1: CRIAÇÃO ---")
        
        # Criar Usuário
        email_teste = f"teste{int(time.time())}@geneslab.com"
        res = requests.post(f"{BASE_URL}/usuarios", json={
            "nome": "Usuário Teste",
            "email": email_teste,
            "senha": "senha_segura_123"
        })
        if res.status_code == 201:
            user_id = res.json().get('id')
            imprimir_log("Criar Usuário", "SUCESSO", f"(ID: {user_id} - Email: {email_teste})")
        else:
            raise Exception(f"Falha ao criar usuário: {res.text}")

        # Criar Categoria
        res = requests.post(f"{BASE_URL}/categorias", json={
            "nome": "Categoria Inicial",
            "id_usuario": user_id
        })
        if res.status_code == 201:
            cat_id = res.json().get('id')
            imprimir_log("Criar Categoria", "SUCESSO", f"(ID: {cat_id})")
        else:
            raise Exception(f"Falha ao criar categoria: {res.text}")

        # Criar Tarefa
        res = requests.post(f"{BASE_URL}/tarefas", json={
            "descricao": "Configurar integração de eventos",
            "id_usuario": user_id,
            "id_categoria": cat_id
        })
        if res.status_code == 201:
            tarefa_id = res.json().get('id')
            imprimir_log("Criar Tarefa", "SUCESSO", f"(ID: {tarefa_id})")
        else:
            raise Exception(f"Falha ao criar tarefa: {res.text}")
        
        # ---------------------------------------------------------
        # AUTENTICAÇÃO (POST /api/login)
        # ---------------------------------------------------------
        print("\n--- ETAPA DE AUTENTICAÇÃO (LOGIN) ---")
        
        # Teste A: Login com Sucesso
        res_login = requests.post(f"{BASE_URL}/api/login", json={
            "email": email_teste,
            "senha": "senha_segura_123"
        })
        if res_login.status_code == 200:
            imprimir_log("Login Válido", "SUCESSO", f"(Mensagem: {res_login.json().get('mensagem')})")
        else:
            raise Exception(f"Falha ao realizar login válido: {res_login.text}")

        # Teste B: Login Inválido (Senha Errada)
        res_login_erro = requests.post(f"{BASE_URL}/api/login", json={
            "email": email_teste,
            "senha": "senha_errada_propositalmente"
        })
        if res_login_erro.status_code == 401:
            imprimir_log("Login Inválido", "SUCESSO", "(Bloqueio de senha incorreta confirmado)")
        else:
            raise Exception(f"Falha de segurança! API permitiu login com senha errada ou retornou status incorreto: {res_login_erro.status_code}")


        # ---------------------------------------------------------
        # 2. EDIÇÃO (PUT)
        # ---------------------------------------------------------
        print("\n--- ETAPA 2: EDIÇÃO ---")

        # Editar Usuário
        res = requests.put(f"{BASE_URL}/usuarios/{user_id}", json={
            "nome": "Usuário Teste Editado"
        })
        imprimir_log("Editar Usuário", "SUCESSO" if res.status_code == 200 else "ERRO", res.text)

        # Editar Categoria
        res = requests.put(f"{BASE_URL}/categorias/{cat_id}", json={
            "nome": "Categoria Editada"
        })
        imprimir_log("Editar Categoria", "SUCESSO" if res.status_code == 200 else "ERRO", res.text)

        # Editar Tarefa
        res = requests.put(f"{BASE_URL}/tarefas/{tarefa_id}", json={
            "descricao": "Configurar integração de eventos (CONCLUÍDO)",
            "concluida": True
        })
        imprimir_log("Editar Tarefa", "SUCESSO" if res.status_code == 200 else "ERRO", res.text)


        # ---------------------------------------------------------
        # 3. VERIFICAÇÃO (GET)
        # ---------------------------------------------------------
        print("\n--- ETAPA 3: VERIFICAÇÃO ---")
        res = requests.get(f"{BASE_URL}/tarefas?id_usuario={user_id}")
        tarefas = res.json()
        print(f"Tarefas encontradas para o usuário {user_id}:")
        for t in tarefas:
            status_txt = "[SUCESSO] Concluída" if t['concluida'] else "[ERRO] Pendente"
            print(f"  -> {status_txt} | {t['descricao']}")


        # ---------------------------------------------------------
        # 4. EXCLUSÃO (DELETE)
        # ---------------------------------------------------------
        print("\n--- ETAPA 4: EXCLUSÃO ---")

        # Deletar Tarefa
        res = requests.delete(f"{BASE_URL}/tarefas/{tarefa_id}")
        imprimir_log("Deletar Tarefa", "SUCESSO" if res.status_code == 200 else "ERRO", res.text)

        # Deletar Categoria
        res = requests.delete(f"{BASE_URL}/categorias/{cat_id}")
        imprimir_log("Deletar Categoria", "SUCESSO" if res.status_code == 200 else "ERRO", res.text)

        # Deletar Usuário
        res = requests.delete(f"{BASE_URL}/usuarios/{user_id}")
        imprimir_log("Deletar Usuário", "SUCESSO" if res.status_code == 200 else "ERRO", res.text)

        print("\n" + "="*50)
        print("[SUCESSO] TODOS OS TESTES PASSARAM COM SUCESSO!")
        print("="*50)

    except requests.exceptions.ConnectionError:
        print("\n[ERRO] ERRO FATAL: Não foi possível conectar ao servidor Flask.")
        print("Certifique-se de que o app.py está rodando (http://127.0.0.1:5000).")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERRO] ERRO FATAL: {str(e)}")
        sys.exit(1)
