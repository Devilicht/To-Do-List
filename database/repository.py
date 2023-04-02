import psycopg2
from os import getenv


class UserRepository:
    def __init__(self):
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            dbname=getenv('POSTGRES_DB'),
            user=getenv('POSTGRES_USER'),
            password=getenv('POSTGRES_PASSWORD')
        )
        cur = conn.cursor()
        self.conn = conn
        self.db = cur

    def findUserByEmail(self, email: str) -> (tuple | None):
        self.db.execute(
            'SELECT user_id, password FROM users WHERE email=%s', (email,))
        result = self.db.fetchone()
        self.conn.commit()
        return result

    def saveUser(self, name: str, email: str, hashed_password: str) -> None:
        self.db.execute(
            'INSERT INTO users (name,email, password) VALUES (%s,%s,%s)', (name, email, hashed_password))
        self.conn.commit()

    def joinUserTask(self, user_id: int):
        self.db.execute(
            'SELECT tasks.task_id, tasks.title, tasks.description, tasks.is_done FROM tasks INNER JOIN users ON tasks.user_id = users.user_id WHERE users.user_id = %s', user_id)
        return self.db.fetchall()

    def generateTask(self, title: str, description: str, user_id: int):
        self.db.execute(
            'INSERT INTO tasks (title, description, user_id) VALUES (%s, %s, %s)', (title, description, user_id))
        self.conn.commit()

    def selectTaskById(self, user_id: int, task_id: int):

        self.db.execute(
            'SELECT * FROM tasks WHERE task_id=%s AND user_id=%s', (task_id, user_id))
        task = self.db.fetchone()
        return task

    def deleteTask(self, task_id: int) -> None:
        self.db.execute('DELETE FROM tasks WHERE task_id=%s', (task_id,))
        self.conn.commit()

    def updateTask(self, title: str, description: str, task_id: str, task: str):
        if title == None and description == None:
            self.db.execute(
                'UPDATE tasks SET title=%s, description=%s WHERE task_id=%s', (task[1], task[2], task_id))
            self.conn.commit()
        elif title == None and description != None:
            self.db.execute(
                'UPDATE tasks SET title=%s, description=%s WHERE task_id=%s', (task[1], description, task_id))
            self.conn.commit()
        elif title != None and description == None:
            self.db.execute(
                'UPDATE tasks SET title=%s, description=%s WHERE task_id=%s', (title, task[2], task_id))
            self.conn.commit()
        else:
            self.db.execute(
                'UPDATE tasks SET title=%s, description=%s WHERE task_id=%s', (title, description, task_id))
            self.conn.commit()
