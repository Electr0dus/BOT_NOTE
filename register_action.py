from aiogram.dispatcher.filters.state import State, StatesGroup


#Машина состояния для регистрации
class RegisterAction(StatesGroup):
    name = State()

#Машина состояния для записи задачи в БД
class WriteEvent(StatesGroup):
    task = State()
    time = State()

#Машина состояния для удаления задачи из БД
class DeleteEvent(StatesGroup):
    event = State()