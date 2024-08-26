import sqlite3

conn_task = sqlite3.connect('events.db')
cur_task = conn_task.cursor()
cur_task.execute('PRAGMA foreign_keys=ON')
conn_task.commit()


# Создание таблицы для хранения задачи времени и айди пользователя
def create_table_task():
    cur_task.execute("""
    CREATE TABLE IF NOT EXISTS task( 
        task TEXT,
        time TEXT,
        id_name INT,
        FOREIGN KEY (id_name) REFERENCES register(id_name)
    );
    """)
    conn_task.commit()


# Записать задачу в БД
def write_event_for_db(event, time, id_user):
    cur_task.execute('INSERT INTO task (task, time, id_name) VALUES (?, ?, ?)', (event, time, id_user,))
    conn_task.commit()


# Получить список записанных задач из БД
def get_event_for_user(id_user):
    cur_task.execute('SELECT task, time FROM task WHERE id_name == ?', (id_user,))
    data_task = cur_task.fetchall()
    # Если список пуст, значит событий нет
    if len(data_task) == 0:
        return '0'
    str_data = ''
    for data in data_task:
        for d_ in data:
            str_data += f'{d_} '
        str_data += '\n'
    conn_task.commit()
    return str_data


# Удалить задачу из БД
def delete_event(event):
    cur_task.execute('DELETE FROM task WHERE task == ?', (event,))
    conn_task.commit()


# Получить список всех значений времени по ID пользователя
def get_time_event():
    cur_task.execute('SELECT time FROM task')
    data_time = cur_task.fetchall()
    # Если нет ниодной записи то вернуть 0
    if len(data_time) == 0:
        return []
    list_time = []
    for time in data_time:
        for t_ in time:
            list_time.append(t_)
    return list_time


# Получить текущую задачу и пользователя от текущего времени
def get_task_for_user(current_time):
    cur_task.execute('SELECT task, id_name FROM task WHERE time = ?', (current_time,))
    data = cur_task.fetchall()
    return data

# Удалить задачу пользователя, после её выполнения
def delete_event_for_user(event, user_id):
    cur_task.execute('DELETE FROM task WHERE task == ? and id_name == ?', (event, user_id,))
    conn_task.commit()
