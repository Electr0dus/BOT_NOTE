import sqlite3

conn_reg = sqlite3.connect('events.db')
cur_reg = conn_reg.cursor()
cur_reg.execute('PRAGMA foreign_keys=ON')
conn_reg.commit()


#Создание таблицы для регистрации пользователей
def create_table_register():
    cur_reg.execute('''
    CREATE TABLE IF NOT EXISTS register(
        id_name INT PRIMARY KEY,
        username TEXT NOT NULL
    );
    ''')
    conn_reg.commit()

#Функция проверки наличия пользователя в БД для предотвращения двойной регестрации
def check_id_name(id_user):
    cur_reg.execute('SELECT id_name FROM register')
    all_id = cur_reg.fetchall()
    for id_ in all_id:
        for id_val in id_:
            if id_user == id_val:
                return False
    return True


#Функция для добавления нового пользователя в БД
def add_user(username, id_name):
    cur_reg.execute('INSERT INTO register (username, id_name) VALUES (?, ?)', (username, id_name))
    conn_reg.commit()

#Функция получения списка пользователей зарегестрированых в БОТе
def get_user():
    cur_reg.execute('SELECT id_name FROM register')
    data_id_user = cur_reg.fetchall()
    user_list = []
    for data_user in data_id_user:
        for data in data_user:
            user_list.append(data)
    return user_list
