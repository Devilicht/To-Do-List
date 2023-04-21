# To-do-list é uma API REST- Flask:

Esta é um API simples para registro de usuários e gerenciamento de tarefas usando Flask e PostgreSQL pelo Docker. Ele inclui rotas para registro de usuário, autenticação, obtenção do ID do usuário logado, leitura, criação, atualização e exclusão de tarefas. A API usa tokens JWT para autenticação e autorização do usuário.

## A API usa as seguintes tecnologias e conceitos:

- Flask: um framework web Python usado para construir uma aplicação web.

- psycopg2: um adaptador PostgreSQL para a linguagem de programação Python.

- JWT: um token web JSON usado para autenticação e autorização do usuário.

- werkzeug.security: uma biblioteca usada para hashing e verificação de senhas.

## Como usar :

Será criar um arquivo ".env" e definir as variaveis, em seguida "subir" o conteiner no docker, assim ja vai estar disponivel o banco de dados para operação e você tambem ja pode se conectar ao banco com as info do ".env".

A API usa o json para sua comunicação, sendo assim nas rotas:

- /register:  metodo utilizado será o **POST**. É necessario  enviar no corpo da solicitação o "name", "email", "password" e "confirm_password".

- /login: metodo utilizado será o **POST**. É necessario com o  enviar no corpo da solicitação o "email" e "password", como resposta recebera um token e deverá colocar no Headers com o parametro de "Authorization" e o value será o token.

- /getLoggedUserId: metodo utilizado **GET**. A partir do token na headers será retornado como resposta o usuario correspondente à aquele token e esse id que usara no "user_id" das próximas rotas.

- /login/<user_id>/tasks: Aqui será usado o "user_id" como parametro e essa rota possui dois metodos.
 O **POST** que é usado para criar uma task, que precisa receber no corpo da solicitação o "title" e "description";
 O **GET** que te retornar todas as tasks criadas com esse "user_id".

- /login/<user_id>/tasks/<task_id>: Aqui você precisara passar o "task_id" que será fornecido no **GET** da rota "/login/<user_id>/tasks". Nessa rota é utilizado dois metodos.
O **PUT** que é usado para alteração da task passada no "task_id", para isso precisa ser enviado no corpo da solicitação o "title" ou a "description".
O **DELETE** que é usado para excluisão da a task passada no "task_id".

## Configuração Database:

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
