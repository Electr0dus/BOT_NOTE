import requests

API_KEY = 'WWOESUDA5UE2'
URL = f'http://api.timezonedb.com/v2.1/get-time-zone?key=WWOESUDA5UE2&format=json&by=zone&zone=Europe/Moscow'


#Функция возвращает текущее время в формате "2024-19-08 14:30" Опрашивать не чаще 1 раз в 1 сек
def get_time():
    responce = requests.get('http://api.timezonedb.com/v2.1/get-time-zone?key=WWOESUDA5UE2&format=json&by=zone&zone=Europe/Moscow')
    if responce.status_code != 200:
        # Вывести в бот сообщение об ошибке
        return 0
    data = responce.json()
    data = data['formatted']
    data = data[:16]
    return data

