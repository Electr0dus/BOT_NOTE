import CRUD_register
import CRUD_task
import key_board
import texts
from register_action import *

# Создаём таблицы
CRUD_register.create_table_register()
CRUD_task.create_table_task()

USER_ID = 0

#Функция запуска бота
async def start_func(message):
    await message.answer(text=texts.START)

#Функция регистрации пользователя
async def register_func(message):
    await message.answer(text=texts.REGISTER_NAME)
    await RegisterAction.name.set()


#Функция для записи имени пользователя в БД
async def register_user(message, state):
    await state.update_data(user_name=message.text)
    # сделать запись в БД с именем пользователя и создать отдельное БД для данного пользователя файл БД должен называться как его имя в трансклипции
    name = await state.get_data()  # get name user
    # проверить на наличие пользователя, чтобы не было повторной регистрации
    if CRUD_register.check_id_name(message.from_user.id):
        CRUD_register.add_user(name['user_name'], message.from_user.id)
    else:
        await message.answer(text=texts.CHECK_USER, reply_markup=key_board.kb)
        await state.finish()
        return
    await message.answer(text=texts.SUCCES_REGISTER, reply_markup=key_board.kb)
    await state.finish()


#Функция для активации состояния для записи задачи в БД
async def write_event(message):
    await WriteEvent.task.set()
    await message.answer(text=texts.WRITE_EVENT)

#Функция записи задачи в БД
async def write_event_state(message, state):
    await state.update_data(task=message.text)
    await message.answer(text=texts.TIME_EVENT)
    await WriteEvent.time.set()


#Функция записи времени выполнения задачи в БД
async def write_time_event(message, state):
    await state.update_data(time=message.text)
    data_event = await state.get_data()
    CRUD_task.write_event_for_db(data_event['task'], data_event['time'], message.from_user.id)
    await message.answer(text=texts.ADD_TASK, reply_markup=key_board.kb)
    await state.finish()


#Функция для проверки текущих задач в БД
async def get_task(message):
    data_task = CRUD_task.get_event_for_user(message.from_user.id)
    #Если в БД нет задачб вывести сообщение об отсутствии текущих задач
    if data_task == '0':
        await message.answer(text=texts.NOT_EVENTS)
        return 0
    await message.answer(text=data_task)


#Функция активации состояния для удаления задачи
async def delete_task_state(message, state):
    await message.answer(text=texts.DELETE_EVENT)
    await DeleteEvent.event.set()

#Функция удаления задачи из БД
async def delete_event(message, state):
    await state.update_data(event=message.text)
    data_event = await state.get_data()
    CRUD_task.delete_event(data_event['event'])
    await message.answer(text=texts.SESCESS_DELETE, reply_markup=key_board.kb)
    await state.finish()



