# Projeto: Sistema de Gerenciamento de Tarefas (Agile & DevOps)

## 1. Descrição do Projeto
Este é um **Sistema de Gerenciamento de Tarefas Web** desenvolvido como parte de um exercício prático de DevOps e metodologias ágeis. O software permite que o usuário gerencie suas atividades pessoais de forma privada, com suporte a categorias, prazos e controle de status, tudo acessível via navegador.

## 2. User Stories (Planejamento Scrum)
Com base na entrevista de levantamento de requisitos, definimos as seguintes histórias de usuário:

* **US01:** Como usuário, quero realizar login para acessar minhas tarefas de forma privada. 
* **US02:** Como usuário, quero cadastrar uma tarefa com descrição, categoria, data de início e conclusão. 
* **US03:** Como usuário, quero visualizar minhas tarefas em uma lista ordenada pelas mais recentes.
* **US04:** Como usuário, quero marcar uma tarefa como concluída para acompanhar meu progresso.
* **US05:** Como usuário, quero editar ou excluir tarefas existentes para manter minha lista atualizada.
* **US05:** Como usuário, quero ver as tarefas em aberto e as concluídas separadamente.

## 3. Product Backlog
Estes itens compõem o backlog inicial e estão vinculados às Issues do repositório:

1.  **Dados:** Criar Modelagem de Banco de Dados (Descrição, Status, Categoria, Datas). 
2.  **Backend:** Realizar integração com o banco de dados escolhido, para trazer os dados gravados.
3.  **Backend:** Desenvolver API REST que implemente um CRUD das tabelas do banco de dados.
4.  **Backend:** Implementar Sistema de Autenticação e Login na API.
5.  **Frontend:** Implementar tela de Login para autenticação com a API.
6.  **Frontend:** Desenvolver Interface (formulário) de Criação de Tarefas.
7.  **Frontend:** Implementar Lista de Tarefas com Ordenação Cronológica, com divisão das tarefas em aberto das concluídas.
8.  **Quality Assurance:** Testar a versão final do sistema, em busca de erros e pontos de correção de bug.

## 4. Organização do Fluxo (Kanban)
O acompanhamento do projeto é feito completamente via **GitHub Projects**, utilizando as colunas:
* **To Do:** Tarefas aguardando início. 
* **In Progress:** Tarefas em desenvolvimento.
* **Review:** Tarefas em fase de teste ou revisão de código.
* **Done:** Tarefas finalizadas e validadas.
