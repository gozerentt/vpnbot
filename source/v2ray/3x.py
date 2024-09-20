import datetime
import json
import requests
import uuid


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

    # Добавление клиентов
    def addClient(self, day, tg_id, user_id):
        epoch = datetime.datetime.utcfromtimestamp(0)
        x_time = int((datetime.datetime.now() - epoch).total_seconds() * 1000.0)
        x_time += 86400000 * day - 10800000
        header = {"Accept": "application/json"}
        data1 = {
            "id": 1,
            "settings": (
                "{\"clients\":"
                "[{\"id\":\"" + str(uuid.uuid1()) + "\","
                "\"alterId\":90,\"email\":\"" + str(user_id) + "\","
                "\"limitIp\":3,\"totalGB\":0,"
                "\"expiryTime\":" + str(x_time) + ",\"enable\":true,\"tgId\":\"" + str(tg_id) + "\",\"subId\":\"\"}]}"
            )
        }
        resource = self.ses.post(f'{self.host}/panel/api/inbounds/addClient', headers=header, json=data1)
        return resource

    # Изменение клиентов
    def updateClient(self, day, user_id):
        dict_x = self.time_active(user_id)
        for key, val in dict_x.items():
            if key != '0' and val != '0':
                val /= 1000
                val += 10800
                date_x = datetime.datetime.utcfromtimestamp(val)
                epoch = datetime.datetime.utcfromtimestamp(0)
                x_time = int((date_x - epoch).total_seconds() * 1000.0)
                x_time += 86400000 * day - 10800000
                header = {"Accept": "application/json"}
                data1 = {
                    "id": 1,
                    "settings": (
                        "{\"clients\":"
                        "[{\"id\":\"" + str(key) + "\","
                        "\"alterId\":90,\"email\":\"" + str(user_id) + "\","
                        "\"limitIp\":3,\"totalGB\":0,"
                        "\"expiryTime\":" + str(x_time) + ",\"enable\":true,\"tgId\":\"" + str(user_id) + "\",\"subId\":\"\"}]}"
                    )
                }
                resource = self.ses.post(f'{self.host}/panel/api/inbounds/updateClient/{key}', headers=header, json=data1)
                return resource
            else:
                epoch = datetime.datetime.utcfromtimestamp(0)
                x_time = int((datetime.datetime.now() - epoch).total_seconds() * 1000.0)
                x_time += 86400000 * day - 10800000
                header = {"Accept": "application/json"}
                data1 = {
                    "id": 1,
                    "settings": (
                        "{\"clients\":"
                        "[{\"id\":\"" + str(key) + "\","
                        "\"alterId\":90,\"email\":\"" + str(user_id) + "\","
                        "\"limitIp\":3,\"totalGB\":0,"
                        "\"expiryTime\":" + str(x_time) + ",\"enable\":true,\"tgId\":\"" + str(user_id) + "\",\"subId\":\"\"}]}"
                    )
                }
                resource = self.ses.post(f'{self.host}/panel/api/inbounds/updateClient/{key}', headers=header, json=data1)
                return resource

    # Получение ссылки ключа
    def link(self, user_id: str):
        """
        Получение ссылки!
        :param user_id: str
        :return: str
        """
        id = ''
        y = json.loads(self.list()['obj'][0]['settings'])
        for i in y["clients"]:
            if i['email'] == user_id:
                id = i["id"]
                x = json.loads(self.list()['obj'][0]['streamSettings'])
                tcp = x['network']
                reality = x['security']
                val = f"vless://{id}@localhost:403?type={tcp}&security={reality}&pbk=gX_zk_LO1eXzsGcaqN4KLEf0JTID7kM4pK5V1JEC4TM&fp=random&sni=cloudflare.com&sid=91f6&spx=%2F#{user_id}"
                return val

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

vpn=X3()
print(vpn.test_connect())
print(vpn.addClient(31,1324103345,'andy'))
# print(vpn.list())
print(vpn.link('andy'))
