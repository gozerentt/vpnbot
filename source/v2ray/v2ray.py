import datetime
import json
import requests
import uuid
import mysql.connector

from source.v2ray.db import *
from x3 import X3
from db import add_user_into_db

class X3:
    login = "root"
    password = "root"
    host = "http://localhost:32569/ujpZuzzRu57prNo5wtns"
    header = []
    data = {"username": login, "password": password}
    ses = requests.Session()

    # Тестовое соединение
    def test_connect(self):
        response = self.ses.post(f"{self.host}/login", data=self.data)
        return response

    # Список клиентов
    def list(self):
        resource = self.ses.get(f'{self.host}/panel/api/inbounds/list', json=self.data).json()
        return resource

    # Добавление клиента
    def addClient(self, day, tg_id, user_id):
        # Получение текущего списка клиентов
        current_clients = self.list()

        # Преобразуем текущий список в формат, где ключи - это имена пользователей (email)
        client_names = {client['email'] for client in json.loads(current_clients['obj'][0]['settings'])["clients"]}

        epoch = datetime.datetime.fromtimestamp(0, datetime.UTC)
        x_time = int((datetime.datetime.now(datetime.UTC) - epoch).total_seconds() * 1000.0)
        x_time += 86400000 * day - 10800000
        header = {"Accept": "application/json"}

        # Проверка на наличие имени пользователя
        original_user_id = user_id
        suffix = 0
        while user_id in client_names:
            suffix += 1
            user_id = f"{original_user_id}_{suffix}"

        data1 = {
            "id": 1,
            "settings": (
                    "{\"clients\":"
                    "[{\"id\":\"" + str(uuid.uuid1()) + "\","
                                                        "\"alterId\":90,\"email\":\"" + str(user_id) + "\","
                                                                                                       "\"limitIp\":1,\"totalGB\":0,"
                                                                                                       "\"expiryTime\":" + str(
                x_time) + ",\"enable\":true,\"tgId\":\"" + str(tg_id) + "\",\"subId\":\"\"}]}"
            )
        }
        resource = self.ses.post(f'{self.host}/panel/api/inbounds/addClient', headers=header, json=data1)

        return user_id  # Возвращаем актуальное имя пользователя

    # Изменение клиентов
    def updateClient(self, month, user_id):
        # Получаем информацию о пользователе по user_id
        user_info = get_user_info_by_id(user_id)

        if not user_info or len(user_info) == 0:
            print(f"Пользователь с id {user_id} не найден.")
            return

        # Извлекаем vpn_string из user_info
        vpn_string = user_info[0]['vpn_string']  # Получаем первый элемент списка

        # Получаем текущую дату и устанавливаем её как дату покупки
        purchase_date = datetime.datetime.now().strftime("%Y-%m-%d")

        # Обновляем purchase_date в БД
        update_purchase_date_in_db(id=user_id, purchase_date=purchase_date)

        # Обновляем время в VPN
        header = {"Accept": "application/json"}

        # Вычисляем новое время окончания подписки
        new_expiry_time = int(datetime.datetime.now().timestamp()) + (month * 30 * 86400)

        # Формируем данные для обновления клиента в VPN
        data1 = {
            "id": 1,
            "settings": (
                "{\"clients\":"
                f"[{{\"id\":\"{vpn_string}\",\"alterId\":90,\"email\":\"{vpn_string}\","
                f"\"limitIp\":3,\"totalGB\":0,\"expiryTime\":{new_expiry_time},"
                "\"enable\":true,\"tgId\":\"\",\"subId\":\"\"}}]}"
            )
        }

        resource = self.ses.post(f'{self.host}/panel/api/inbounds/updateClient/{vpn_string}', headers=header,
                                 json=data1)
        return resource

    # Получение информации о пользователе по vpn_string
    def get_user_info_by_vpn_string(self, vpn_string):
        response = self.list()
        y = json.loads(response['obj'][0]['settings'])

        for client in y["clients"]:
            if client['tgId'] == vpn_string:  # Предполагается, что tgId - это vpn_string
                return client  # Возвращаем информацию о клиенте

        return None  # Если не найдено

    # Получение ссылки ключа
    def link(self, user_id: str):
        """
        Получение ссылки!
        :param user_id: str
        :return: str
        """
        id = ''
        response = self.list()

        # Получаем список клиентов из правильного места
        y = json.loads(response['obj'][0]['settings'])

        # Создаем словарь email: id
        possible_emails = {client['email']: client['id'] for client in y["clients"]}

        # Проверяем наличие пользователя с именем, включая суффиксы
        if user_id in possible_emails:
            id = possible_emails[user_id]
        else:
            # Если не найден, проверяем все возможные суффиксы
            for email in possible_emails:
                if email.startswith(user_id + "_"):  # Проверяем, начинается ли email с user_id + "_"
                    id = possible_emails[email]
                    break

        # Если id найден, формируем ссылку
        if id:
            x = json.loads(response['obj'][0]['streamSettings'])
            tcp = x['network']
            reality = x['security']
            val = f"vless://{id}@localhost:403?type={tcp}&security={reality}&pbk=gX_zk_LO1eXzsGcaqN4KLEf0JTID7kM4pK5V1JEC4TM&fp=random&sni=cloudflare.com&sid=91f6&spx=%2F#{user_id}"
            return val

        return None  # Если пользователь не найден, возвращаем None

    # Проверка времени активной подписки
    def time_active(self, user_id: str):
        dict_x = {}
        epoch = datetime.datetime.utcfromtimestamp(0)
        x_time = int((datetime.datetime.now() - epoch).total_seconds() * 1000.0)
        y = json.loads(self.list()['obj'][0]['settings'])
        for i in y["clients"]:
            if i['email'] == user_id:
                if i['enable'] and i['expiryTime'] > x_time:
                    dict_x[i['id']] = i['expiryTime']
                    return dict_x
                else:
                    dict_x[i['id']] = '0'
                    return dict_x
        if len(dict_x) == 0:
            dict_x['0'] = '0'
        return dict_x

    # Проверка активности
    def activ(self, user_id: str):
        """
        Проверка активности подписки
        :param user_id: str
        :return: str
        """
        dict_x = {}
        epoch = datetime.datetime.utcfromtimestamp(0)
        x_time = int((datetime.datetime.now() - epoch).total_seconds() * 1000.0)
        y = json.loads(self.list()['obj'][0]['settings'])
        for i in y["clients"]:
            if i['email'] == user_id:
                if i['enable'] and i['expiryTime'] > x_time:
                    print(i)
                    print(i['enable'])
                    dict_x['activ'] = 'Активен'
                    ts = i['expiryTime']
                    ts /= 1000
                    ts += 10800
                    dict_x['time'] = datetime.datetime.utcfromtimestamp(ts).strftime('%d-%m-%Y %H:%M') + ' МСК'
                    return dict_x
                else:
                    print(i)
                    print(i['enable'])
                    dict_x['activ'] = 'Не Активен'
                    ts = i['expiryTime']
                    ts /= 1000
                    ts += 10800
                    dict_x['time'] = datetime.datetime.utcfromtimestamp(ts).strftime('%d-%m-%Y %H:%M') + ' МСК'
                    return dict_x
        dict_x['activ'] = 'Не зарегистрирован'
        dict_x['time'] = '-'
        return dict_x

    # Проверка активных пользователей с подпиской
    def activ_list(self):
        """
        Проверка активности подписки
        :param user_id: str
        :return: str
        """
        dict_x = {}
        y = json.loads(self.list()['obj'][0]['settings'])
        for i in y["clients"]:
            ts = i['expiryTime']
            ts /= 1000
            ts += 10800
            x = datetime.datetime.now()
            y = datetime.datetime.utcfromtimestamp(ts)
            z = y - x
            dict_x[i['email']] = z.days
        return dict_x

    # Добавить пользователя в VPN и MySQL
    def add_x3_db(self, tg_id, tg_name):
        user_id = self.addClient(31, tg_id, tg_name)  # Теперь user_id будет актуальным именем пользователя с суффиксом
        # Получаем ссылку с учетом суффикса
        vpn_string = self.link(user_id)  # Используем user_id, возвращаемый addClient
        # Добавляем пользователя в базу
        add_user_into_db(tg_id, datetime.datetime.now().strftime("%Y-%m-%d"), vpn_string)

    # def add_x3_db(self,tg_id,tg_name):
    #     self.addClient(31,tg_id,tg_name)
    #     add_user_into_db(tg_id,datetime.datetime.now().strftime("%Y-%m-%d"),str(self.link(tg_name)))

x3_inst=X3()
print(x3_inst.test_connect())
# x3_inst.add_x3_db(tg_id='1324103344',tg_name='anton')
# print(get_vpn_tokens('1324103344'))
x3_inst.updateClient(3,'32')