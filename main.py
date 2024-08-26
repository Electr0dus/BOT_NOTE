import asyncio

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import CRUD_register
import CRUD_task
# Пользовательские модули
import RTC_return
import config
import function
from register_action import *

bot = Bot(token=config.TOKEN_TG)
dp = Dispatcher(bot, storage=MemoryStorage())

# Бот делает действие по команде /start
dp.message_handler(commands=['start'])(function.start_func)
# Бот делает действие по команде /register
dp.message_handler(commands=['register'])(function.register_func)
# Активируется состояние для записи имени пользователя
dp.message_handler(state=RegisterAction.name)(function.register_user)
# Активируется по нажатию кнопки "Записать событие"
dp.message_handler(text=['Записать событие'])(function.write_event)
# Активируется состояние для записи задачи в БД
dp.message_handler(state=WriteEvent.task)(function.write_event_state)
# Активируется состояние для записи времени в БД
dp.message_handler(state=WriteEvent.time)(function.write_time_event)
# Активируется по нажатию кнопки "Просмотреть события"
dp.message_handler(text=['Просмотреть события'])(function.get_task)
# Активируется по нажатию кнопки "Удалить событие"
dp.message_handler(text=['Удалить событие'])(function.delete_task_state)
# Активируется состояние для удаления задачи
dp.message_handler(state=DeleteEvent.event)(function.delete_event)


# Функция для проверки совпадения времени с текущей задачей
async def check_task_for_time():
    while True:
        # # Проверить наличие на зарегестрированных пользователей
        # # если длина списка больше нуля, значит пользователи есть
        # if len(CRUD_register.get_user()) > 0:
            # Получить список всех временных значений
        all_time = CRUD_task.get_time_event()
        print(all_time)
        data = RTC_return.get_time()
            # Если время есть в списке, то отправить задачу пользователю с помощью сообщения
        if data in all_time:
                # Отправить задачу ответным сообщением
            data_user = CRUD_task.get_task_for_user(data)  # Получить задание и пользователя, кому это принадлежит
                # data_user[0][0] - хранит текущую задачу
                # data_user[0][1] - хранит ID пользователя
                # Отправить сообщение пользователю о текущей задаче
            await bot.send_message(chat_id=data_user[0][1], text=data_user[0][0])
            CRUD_task.delete_event_for_user(data_user[0][0], data_user[0][1])
                # удалить отправленную задачу
        print(data)
        await asyncio.sleep(60)



# Сделать функцию для опроса времени с API и проверки на наличие времени каждую минуту или меньше!!

# Опрашивать значение только если пользователь зарегестрировался и отправлять сообщение обратно зарегестрированным пользователям
# if len(CRUD_register.get_user()) > 0:
#     print(CRUD_task.get_time_event())
# Получать текущее время 1 раз в 1.5 сек
# if len(CRUD_task.get_time_event()) > 0:
#     print(RTC_return.get_time())

async def main(_):
    asyncio.create_task(check_task_for_time())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=main)
