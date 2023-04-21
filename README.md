# API REST- Flask

Esta é um API simples para registro de usuários e gerenciamento de tarefas usando Flask e PostgreSQL pelo Docker. Ele inclui rotas para registro de usuário, autenticação, obtenção do ID do usuário logado, leitura, criação, atualização e exclusão de tarefas. A API usa tokens JWT para autenticação e autorização do usuário.

# A API usa as seguintes tecnologias e conceitos:

- Flask: um framework web Python usado para construir uma aplicação web.

- psycopg2: um adaptador PostgreSQL para a linguagem de programação Python.

- JWT: um token web JSON usado para autenticação e autorização do usuário.

- werkzeug.security: uma biblioteca usada para hashing e verificação de senhas.

# A API possui as seguintes rotas:

- /register: uma rota para registro de usuário.

- /users: uma rota para autenticação de usuário.

- /getLoggedUserId: uma rota para obter o ID do usuário logado.

- /users/<user_id>/tasks: uma rota para leitura, criação, atualização e exclusão de tarefas. O ID do usuário é passado como parâmetro.

A API permite que os usuários criem uma conta, façam login, criem tarefas, leiam informações sobre tarefas, atualizem informações de tarefas e excluam tarefas. Somente usuários logados podem acessar as rotas de tarefas.

# Configuração Database:
Em relação a criação da DB foram criadas duas tabelas:
- CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(150) NOT NULL
);

- CREATE TABLE tasks (
    task_id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NULL,
    is_done BOOLEAN DEFAULT false,
    user_id INTEGER REFERENCES users(user_id)
);
