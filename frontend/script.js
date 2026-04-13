const API = "http://127.0.0.1:5000";

/* LOGIN */

async function login() {
    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;

    if (!email || !senha) {
        alert("Preencha email e senha");
        return;
    }

    try {
        const res = await fetch(`${API}/login`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ email, senha })
        });

        const data = await res.json();

        if (res.ok) {
            localStorage.setItem("usuario_id", data.id);
            localStorage.setItem("usuario_nome", data.nome);
            window.location.href = "tasks.html";
        } else {
            alert(data.erro || "Erro ao fazer login");
        }
    } catch (error) {
        console.error("Erro:", error);
        alert("Erro de conexão com o servidor");
    }
}

function mostrarCadastro() {
    document.getElementById("login-box").style.display = "none";
    document.getElementById("cadastro-box").style.display = "block";
}

function mostrarLogin() {
    document.getElementById("login-box").style.display = "block";
    document.getElementById("cadastro-box").style.display = "none";
}

async function criarUsuario() {
    const nome = document.getElementById("nome").value;
    const email = document.getElementById("novo_email").value;
    const senha = document.getElementById("nova_senha").value;

    if (!nome || !email || !senha) {
        alert("Preencha todos os campos");
        return;
    }

    try {
        const res = await fetch(`${API}/usuarios`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ nome, email, senha })
        });

        if (res.ok) {
            alert("Usuário criado! Faça login.");
            mostrarLogin();
        } else {
            const data = await res.json();
            alert(data.erro || "Erro ao criar usuário");
        }
    } catch (error) {
        console.error("Erro:", error);
        alert("Erro de conexão com o servidor");
    }
}

/* UTILS */

function getUserId() {
    return localStorage.getItem("usuario_id");
}

function logout() {
    localStorage.clear();
    window.location.href = "index.html";
}

/* TOGGLE DO TAREFA*/

function toggleFormTarefa() {
    const bloco = document.getElementById("blocoNovaTarefa");
    const btn = document.getElementById("toggleFormBtn");
    
    if (bloco.classList.contains("visivel")) {
        bloco.classList.remove("visivel");
        btn.textContent = "+ Nova Tarefa";
    } else {
        bloco.classList.add("visivel");
        btn.textContent = "− Fechar";
    }
}

/* CATEGORIAS */

async function carregarCategorias() {
    try {
        const res = await fetch(`${API}/categorias`);
        const categorias = await res.json();

        const lista = document.getElementById("categorias");
        const select = document.getElementById("categoria_select");

        if (!lista || !select) return;

        lista.innerHTML = "";
        select.innerHTML = '<option value="">Sem categoria</option>';

        const userId = getUserId();
        categorias
            .filter(c => c.id_usuario == userId)
            .forEach(c => {
                const li = document.createElement("li");
                li.className = "categoria-tag";
                li.innerHTML = `
                    ${c.nome}
                    <button onclick="editarCategoria(${c.id}, '${c.nome.replace(/'/g, "\\'")}')">✎</button>
                    <button onclick="deletarCategoria(${c.id})">×</button>
                `;
                lista.appendChild(li);

                const opt = document.createElement("option");
                opt.value = c.id;
                opt.innerText = c.nome;
                select.appendChild(opt);
            });
    } catch (error) {
        console.error("Erro ao carregar categorias:", error);
    }
}

async function criarCategoria() {
    const nome = document.getElementById("cat_nome").value;
    if (!nome) return;

    try {
        await fetch(`${API}/categorias`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                nome,
                id_usuario: getUserId()
            })
        });

        document.getElementById("cat_nome").value = "";
        carregarCategorias();
    } catch (error) {
        console.error("Erro ao criar categoria:", error);
    }
}

async function editarCategoria(id, nomeAtual) {
    const novoNome = prompt("Novo nome:", nomeAtual);
    if (!novoNome || novoNome === nomeAtual) return;

    try {
        await fetch(`${API}/categorias/${id}`, {
            method: "PUT",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ nome: novoNome })
        });

        carregarCategorias();
    } catch (error) {
        console.error("Erro ao editar categoria:", error);
    }
}

async function deletarCategoria(id) {
    if (!confirm("Tem certeza que deseja excluir esta categoria?")) return;
    
    try {
        await fetch(`${API}/categorias/${id}`, { method: "DELETE" });
        carregarCategorias();
    } catch (error) {
        console.error("Erro ao deletar categoria:", error);
    }
}

/* TAREFAS */

async function criarTarefa() {
    const descricao = document.getElementById("desc").value;
    const data_inicio = document.getElementById("data_inicio").value || null;
    const data_fim = document.getElementById("data_fim").value || null;
    const categoria_id = document.getElementById("categoria_select").value || null;

    if (!descricao) {
        alert("A descrição da tarefa é obrigatória");
        return;
    }

    try {
        await fetch(`${API}/tarefas`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                descricao,
                id_usuario: getUserId(),
                id_categoria: categoria_id,
                data_inicio,
                data_fim
            })
        });

        document.getElementById("desc").value = "";
        document.getElementById("data_inicio").value = "";
        document.getElementById("data_fim").value = "";
        
        // esconder o form depois de cirar
        const bloco = document.getElementById("blocoNovaTarefa");
        bloco.classList.remove("visivel");
        document.getElementById("toggleFormBtn").textContent = "+ Nova Tarefa";
        
        carregarTarefas();
    } catch (error) {
        console.error("Erro ao criar tarefa:", error);
    }
}

async function carregarTarefas() {
    try {
        const res = await fetch(`${API}/tarefas?id_usuario=${getUserId()}`);
        let tarefas = await res.json();

        const status = document.getElementById("filtro_status")?.value;
        const ordenacao = document.getElementById("filtro_ordenacao")?.value;

        // filtro
        if (status === "pendente") {
            tarefas = tarefas.filter(t => !t.concluida);
        }
        if (status === "concluida") {
            tarefas = tarefas.filter(t => t.concluida);
        }

        // ordenação
        if (ordenacao === "recentes") {
            tarefas.sort((a, b) => (b.id || 0) - (a.id || 0));
        } else {
            tarefas.sort((a, b) => (a.id || 0) - (b.id || 0));
        }

        const lista = document.getElementById("lista");
        lista.innerHTML = "";

        if (tarefas.length === 0) {
            lista.innerHTML = `
                <div class="estado-vazio">
                    <div class="icone-vazio">—</div>
                    <p>Nenhuma tarefa encontrada</p>
                    <p class="subtexto">Clique em "+ Nova Tarefa" para começar</p>
                </div>
            `;
            return;
        }

        // buscar categorias para mostrar o nome
        const resCat = await fetch(`${API}/categorias`);
        const categorias = await resCat.json();
        const mapaCategorias = {};
        categorias.forEach(c => { mapaCategorias[c.id] = c.nome; });

        tarefas.forEach(t => {
            const li = document.createElement("li");
            li.className = "item-tarefa";

            const categoriaNome = t.id_categoria ? mapaCategorias[t.id_categoria] : null;
            const statusClass = t.concluida ? 'concluida' : '';
            const statusTexto = t.concluida ? 'Concluída' : 'Pendente';

            li.innerHTML = `
                <div class="info-tarefa">
                    <div class="descricao-tarefa ${statusClass}">
                        ${t.descricao}
                        ${categoriaNome ? `<span class="categoria-tag-tarefa">${categoriaNome}</span>` : ''}
                    </div>
                    <div class="meta-tarefa">
                        <div class="meta-item">
                            <span class="meta-label">Início:</span>
                            <span>${t.data_inicio ? formatarData(t.data_inicio) : '—'}</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Fim:</span>
                            <span>${t.data_fim ? formatarData(t.data_fim) : '—'}</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Status:</span>
                            <span>${statusTexto}</span>
                        </div>
                    </div>
                </div>
                <div class="acoes-tarefa">
                    ${!t.concluida ? `<button class="btn-concluir" onclick="concluir(${t.id})" title="Marcar como concluída">✓</button>` : ''}
                    <button class="btn-editar" onclick="editarTarefa(${t.id})" title="Editar tarefa">✎</button>
                    <button class="btn-deletar" onclick="deletarTarefa(${t.id})" title="Excluir tarefa">×</button>
                </div>
            `;

            lista.appendChild(li);
        });
    } catch (error) {
        console.error("Erro ao carregar tarefas:", error);
    }
}

async function editarTarefa(id) {
    const novaDesc = prompt("Nova descrição:");
    if (!novaDesc) return;

    try {
        await fetch(`${API}/tarefas/${id}`, {
            method: "PUT",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ descricao: novaDesc })
        });

        carregarTarefas();
    } catch (error) {
        console.error("Erro ao editar tarefa:", error);
    }
}

async function concluir(id) {
    try {
        await fetch(`${API}/tarefas/${id}`, {
            method: "PUT",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ concluida: true })
        });

        carregarTarefas();
    } catch (error) {
        console.error("Erro ao concluir tarefa:", error);
    }
}

async function deletarTarefa(id) {
    if (!confirm("Tem certeza que deseja excluir esta tarefa?")) return;
    
    try {
        await fetch(`${API}/tarefas/${id}`, { method: "DELETE" });
        carregarTarefas();
    } catch (error) {
        console.error("Erro ao deletar tarefa:", error);
    }
}

// aux pra formatar a data
function formatarData(dataString) {
    if (!dataString) return '—';
    
    try {
        const data = new Date(dataString);
        return data.toLocaleDateString('pt-BR', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    } catch {
        return dataString.replace('T', ' ');
    }
}

/* INIT */

window.onload = () => {
    const path = window.location.pathname;

    // se estiver no index não faz nada
    if (path.includes("index")) return;

    // verifica se está logado
    if (!getUserId()) {
        window.location.href = "index.html";
        return;
    }

    // carrega dados da página de tarefas
    if (path.includes("tasks")) {
        carregarCategorias();
        carregarTarefas();
    }
};
