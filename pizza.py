from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api
import sqlite3 as sql
import time
import random

connection = sql.connect("user.sqlite", check_same_thread=False)

q = connection.cursor()
q.execute('''
''')
connection.commit()
connection.close()




vk = vk_api.VkApi(token="")

vk._auth_token()

vk.get_api()

longpoll = VkBotLongPoll(vk, 176533270)


time_boy = datetime.now()
time_work = datetime.now()
while True:
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.object.peer_id == event.object.from_id:
                    id = event.object.peer_id
                    body = event.object.text
                    mesage = event.object.peer_id



                    if body.lower() == "начать" or body.lower() == "помощь":
                        connection = sql.connect("user.sqlite", check_same_thread=False)
                        q = connection.cursor()
                        q.execute("SELECT * FROM user_info WHERE User_ID = '%s'" % (id))
                        result = q.fetchall()
                        if len(result) == 0:
                            user_info = vk.method("users.get", {"user_ids": id, "fields": "first_name"})
                            user_name = user_info[0]["first_name"]
                            print("Time to добавить юзера")
                            q.execute(
                                "INSERT INTO user_info (Name, User_ID, Balance, Ownment, Admin, Yron, Bank) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                                user_name,
                                id, 0, "", 0, 0, 0))
                            connection.commit()
                            connection.close()
                        else:
                            q.execute("SELECT * FROM user_info WHERE User_ID = %s" % (id))
                            result = q.fetchall()
                            print(result)
                            user_name = result[0][1]
                        vk.method("messages.send", {"peer_id": mesage, "message": user_name + """, мои команды:
                    &#127344;Аккаунт:
                        Профиль
                        Ник [Придуманное имя]\n
                    &#128377;Мини-игры:
                        Казино [сумма]
                        Кубик [грань от 1 до 5]\n
                    &#128194;Прочее:
                        Недвижимость [id]:
                        Дом - 1(100000$)
                        Машина - 2(50000$)
                        Дача - 3(40000$)
                        Перевод [id игрока] [Сумма перевода]
                        Магазин
                        Приобрести [номер товара]
                        Арена
                        Банк положить [Сумма вклада]
                        Банк снять [Сумма вывода]""", "random_id": random.randint(1, 2147483647)})



                    elif "кубик" in body.lower():
                        cube = random.randint(1, 5)
                        user_cube = str(body.lower()[-1])
                        user_win = random.randint(7000, 15000)
                        connection = sql.connect("user.sqlite", check_same_thread=False)
                        q = connection.cursor()
                        q.execute("SELECT * FROM user_info WHERE User_ID = %s" % (id))
                        result = q.fetchall()
                        if len(result) == 0:
                            vk.method("messages.send", {"peer_id": mesage, "message": "Вы ещё не зарегистрировались ! Введите команду (начать)", "random_id": random.randint(1, 2147483647)})
                            connection.commit()
                            connection.close()
                        else:
                            q.execute("SELECT * FROM user_info WHERE User_ID = %s" % (id))
                            result = q.fetchall()
                            print(result)
                            user_name = result[0][1]
                            if user_cube == str(cube):
                                vk.method("messages.send", {"peer_id": mesage,
                                                            "message": user_name + ", вы угадали! 😯 Выйгрыш " + str(
                                                                user_win) + "$", "random_id": random.randint(1, 2147483647)})
                                q = connection.cursor()
                                q.execute("SELECT * FROM user_info WHERE User_ID = %s" % (id))
                                result = q.fetchall()
                                q.execute(
                                    "UPDATE user_info SET Balance = '%s' WHERE User_ID = '%s'" % (result[0][3] + user_win, id))
                                connection.commit()
                                connection.close()

                            else:
                                vk.method("messages.send", {"peer_id": mesage,
                                                            "message": user_name + ", вы проиграли! Выпало число " + str(
                                                                cube) + " 😔", "random_id": random.randint(1, 2147483647)})



                    elif "казино" in body.lower():
                        try:
                            kaz = body.lower()[6:]
                            if kaz == "":
                                vk.method("messages.send", {"peer_id": mesage, "message": "Вы не ввели ставку !", "random_id": random.randint(1, 2147483647)})
                            elif int(kaz) <= 0:
                                vk.method("messages.send", {"peer_id": mesage, "message": "Нельзя ставить ставку 0 и ниже нуля", "random_id": random.randint(1, 2147483647)})
                            else:
                                connection = sql.connect('user.sqlite', check_same_thread=False)
                                q = connection.cursor()
                                q.execute("SELECT * FROM user_info WHERE User_ID = %s" % (id))
                                result = q.fetchall()
                                if len(result) == 0:
                                    vk.method("messages.send", {"peer_id": mesage, "message": "Вы ещё не зарегистрировались ! Введите команду (начать)", "random_id": random.randint(1, 2147483647)})
                                    connection.commit()
                                    connection.close()
                                else:
                                    kazino = random.randint(1, 2)
                                    try:
                                        rate = int(body.lower().split("казино ")[-1])
                                        if result[0][3] >= rate:
                                            if kazino == 1:
                                                coefficient = random.randint(1, 3)
                                                if coefficient == 1:
                                                    q.execute("SELECT * FROM user_info WHERE User_ID = %s" % (id))
                                                    result = q.fetchall()
                                                    money = result[0][3]
                                                    connection = sql.connect('user.sqlite', check_same_thread=False)
                                                    q = connection.cursor()
                                                    q.execute("UPDATE user_info SET Balance = '%s' WHERE User_ID = '%s'" % (int(money) +
                                                                                                                            rate * 2, id))
                                                    connection.commit()
                                                    connection.close()
                                                    vk.method("messages.send",
                                                              {"peer_id": mesage, "message": "Вы выиграли " + str(rate * 2) + "!", "random_id": random.randint(1, 2147483647)})
                                                elif coefficient == 2:
                                                    q.execute("SELECT * FROM user_info WHERE User_ID = %s" % (id))
                                                    result = q.fetchall()
                                                    money = result[0][3]
                                                    connection = sql.connect('user.sqlite', check_same_thread=False)
                                                    q = connection.cursor()
                                                    q.execute("UPDATE user_info SET Balance = '%s' WHERE User_ID = '%s'" % (int(money) +
                                                                                                                            rate * 3, id))
                                                    connection.commit()
                                                    connection.close()
                                                    vk.method("messages.send",
                                                              {"peer_id": mesage, "message": "Вы выиграли " + str(rate * 3) + "!", "random_id": random.randint(1, 2147483647)})
                                                else:
                                                    q.execute("SELECT * FROM user_info WHERE User_ID = %s" % (id))
                                                    result = q.fetchall()
                                                    money = result[0][3]
                                                    connection = sql.connect('user.sqlite', check_same_thread=False)
                                                    q = connection.cursor()
                                                    q.execute("UPDATE user_info SET Balance = '%s' WHERE User_ID = '%s'" % (int(money) +
                                                                                                                            rate * 7, id))
                                                    connection.commit()
                                                    connection.close()
                                                    vk.method("messages.send",
                                                              {"peer_id": mesage, "message": "Вы выиграли " + str(rate * 7) + "!", "random_id": random.randint(1, 2147483647)})
                                            elif kazino == 2:
                                                vk.method("messages.send",
                                                          {"peer_id": mesage, "message": "Вы проиграли " + str(rate) + ":(", "random_id": random.randint(1, 2147483647)})
                                                connection = sql.connect('user.sqlite', check_same_thread=False)
                                                q = connection.cursor()
                                                q.execute("UPDATE user_info SET Balance = '%s' WHERE User_ID = '%s'" % (result[0][3] - rate, id))
                                                connection.commit()
                                                connection.close()
                                        else:
                                            vk.method("messages.send",
                                          {"peer_id": mesage, "message": "Недостаточно средств!", "random_id": random.randint(1, 2147483647)})
                                    except:
                                        vk.method("messages.send", {"peer_id": mesage, "message": "Введите корректную сумму ставки!", "random_id": random.randint(1, 2147483647)})


                        except:
                            vk.method("messages.send", {"peer_id": mesage, "message": "Введите корректную сумму ставки!", "random_id": random.randint(1, 2147483647)})



                    elif "недвижимость" in body.lower():
                        try:
                            connection = sql.connect('user.sqlite', check_same_thread=False)
                            q = connection.cursor()
                            q.execute("SELECT * FROM user_info WHERE User_ID = %s" % (id))
                            result = q.fetchall()
                            if len(result) == 0:
                                vk.method("messages.send", {"peer_id": mesage, "message": "Вы ещё не зарегистрировались ! Введите команду (начать)", "random_id": random.randint(1, 2147483647)})
                                connection.commit()
                                connection.close()
                            else:
                                realty = int(body.lower().split("недвижимость")[1])
                                if realty == 1:
                                    connection = sql.connect('user.sqlite', check_same_thread=False)
                                    q = connection.cursor()
                                    q.execute("SELECT * FROM user_info WHERE User_ID = %s" % (id))
                                    result = q.fetchall()
                                    money = result[0][3]
                                    ownment = result[0][4]
                                    if money >= 100000:
                                        if ownment != None:
                                            q.execute("UPDATE user_info SET Ownment = '%s' WHERE User_ID = '%s'" % (
                                            str(ownment) + "1,", id))
                                            q.execute(
                                                "UPDATE user_info SET Balance = '%s' WHERE User_ID = '%s'" % (money - 100000,
                                                                                                              id))
                                            connection.commit()
                                            connection.close()
                                            vk.method("messages.send", {"peer_id": mesage, "message": "Вы купили дом&#127968;!", "random_id": random.randint(1, 2147483647)})
                                        else:
                                            q.execute("UPDATE user_info SET Ownment = '%s' WHERE User_ID = '%s'" % ("1,", id))
                                            q.execute(
                                                "UPDATE user_info SET Balance = '%s' WHERE User_ID = '%s'" % (money - 100000,
                                                                                                              id))
                                            connection.commit()
                                            connection.close()
                                            vk.method("messages.send", {"peer_id": mesage, "message": "Вы купили дом&#127968;!", "random_id": random.randint(1, 2147483647)})
                                    else:
                                        vk.method("messages.send",
                                                  {"peer_id": id, "message": "Недостаточно денег для покупки!", "random_id": random.randint(1, 2147483647)})
                                elif realty == 2:
                                    connection = sql.connect('user.sqlite', check_same_thread=False)
                                    q = connection.cursor()
                                    q.execute("SELECT * FROM user_info WHERE User_ID = %s" % (id))
                                    result = q.fetchall()
                                    money = result[0][3]
                                    ownment = result[0][4]
                                    if money >= 50000:
                                        if ownment != None:
                                            q.execute("UPDATE user_info SET Ownment = '%s' WHERE User_ID = '%s'" % (
                                            str(ownment) + "2,", id))
                                            q.execute(
                                                "UPDATE user_info SET Balance = '%s' WHERE User_ID = '%s'" % (money - 50000,
                                                                                                              id))
                                            connection.commit()
                                            connection.close()
                                            vk.method("messages.send", {"peer_id": mesage, "message": "Вы купили машину!&#128664;", "random_id": random.randint(1, 2147483647)})
                                        else:
                                            q.execute("UPDATE user_info SET Ownment = '%s' WHERE User_ID = '%s'" % ("2,", id))
                                            q.execute(
                                                "UPDATE user_info SET Balance = '%s' WHERE User_ID = '%s'" % (money - 50000,
                                                                                                              id))
                                            connection.commit()
                                            connection.close()
                                            vk.method("messages.send", {"peer_id": mesage, "message": "Вы купили машину!&#128664;", "random_id": random.randint(1, 2147483647)})
                                    else:
                                        vk.method("messages.send",
                                                  {"peer_id": mesage, "message": "Недостаточно денег для покупки!", "random_id": random.randint(1, 2147483647)})
                                elif realty == 3:
                                    connection = sql.connect('user.sqlite', check_same_thread=False)
                                    q = connection.cursor()
                                    q.execute("SELECT * FROM user_info WHERE User_ID = %s" % (id))
                                    result = q.fetchall()
                                    money = result[0][3]
                                    ownment = result[0][4]
                                    if money >= 40000:
                                        if ownment != None:
                                            q.execute("UPDATE user_info SET Ownment = '%s' WHERE User_ID = '%s'" % (
                                            str(ownment) + "3,", id))
                                            q.execute(
                                                "UPDATE user_info SET Balance = '%s' WHERE User_ID = '%s'" % (money - 40000,
                                                                                                              id))
                                            connection.commit()
                                            connection.close()
                                            vk.method("messages.send", {"peer_id": mesage, "message": "Вы купили дачу!&#127969;", "random_id": random.randint(1, 2147483647)})
                                        else:
                                            q.execute("UPDATE user_info SET Ownment = '%s' WHERE User_ID = '%s'" % ("3,", id))
                                            q.execute(
                                                "UPDATE user_info SET Balance = '%s' WHERE User_ID = '%s'" % (money - 40000,
                                                                                                              id))
                                            connection.commit()
                                            connection.close()
                                            vk.method("messages.send", {"peer_id": mesage, "message": "Вы купили дачу!&#127969;", "random_id": random.randint(1, 2147483647)})
                                    else:
                                        vk.method("messages.send",
                                                  {"peer_id": mesage, "message": "Недостаточно денег для покупки!", "random_id": random.randint(1, 2147483647)})
                        except:
                            vk.method("messages.send", {"peer_id": mesage, "message": "Введите корректный id недвижимости!", "random_id": random.randint(1, 2147483647)})



                    elif body.lower() == "профиль":
                        connection = sql.connect('user.sqlite', check_same_thread=False)
                        q = connection.cursor()
                        q.execute("SELECT * FROM user_info WHERE User_ID = %s" % (id))
                        result = q.fetchall()
                        if len(result) == 0:
                            vk.method("messages.send", {"peer_id": mesage, "message": "Вы ещё не зарегистрировались ! Введите команду (начать)", "random_id": random.randint(1, 2147483647)})
                            connection.commit()
                            connection.close()
                        else:
                            q.execute("SELECT * FROM user_info WHERE User_ID = %s" % (id))
                            result = q.fetchall()
                            yron = 0
                            if result[0][7] == 1:
                                yron = '3 - 10'
                            elif result[0][7] == 2:
                                yron = '15 - 35'
                            elif result[0][7] == 3:
                                yron = '45 - 60'
                            elif result[0][7] == 4:
                                yron = '77 - 88'
                            else:
                                yron = '0'
                            user_id = result[0][0]
                            name = result[0][1]
                            balance = result[0][3]
                            ownment = result[0][4]
                            weapon = result[0][5]
                            admin = result[0][6]
                            bank = result[0][8]

                            ownment_message = ""
                            if ownment != None:
                                ownment = ownment.split(",")
                                ownment = ownment[:-1]
                                for own in ownment:
                                    if int(own) == 1:
                                        ownment_message += "Дом 🏠\n"
                                    elif int(own) == 2:
                                        ownment_message += "Машина 🚘\n"
                                    elif int(own) == 3:
                                        ownment_message += "Дача 🏡\n"
                            vk.method("messages.send", {"peer_id": mesage,
                                                        "message": "&#9762;ID: " + str(user_id) + "\n&#128203;Ваш ник: " + str(name) +
                                                             "\n💰Денег: " + str(balance) + "\n&#128179;Банковский счёт: " + str(bank) +
                                                                   "\nВаши владения:\n " + ownment_message + "\n&#128299;Ваше оружие: " + str(weapon) + "\n&#128165;Урон: " + yron + "\n&#128190;Права Администратора: " + str(admin), "random_id": random.randint(1, 2147483647)})



                    elif "ник" in body.lower():
                        if body.lower()[0:4] == "ник ":
                            connection = sql.connect("user.sqlite", check_same_thread=False)
                            q = connection.cursor()
                            q.execute("SELECT * FROM user_info WHERE User_ID = %s" % (id))
                            result = q.fetchall()
                            if len(result) == 0:
                                vk.method("messages.send", {"peer_id": mesage, "message": "Вы ещё не зарегистрировались ! Введите команду (начать)", "random_id": random.randint(1, 2147483647)})
                                connection.commit()
                                connection.close()
                            else:
                                user_name = body[4:24]
                                if user_name == "":
                                    vk.method("messages.send", {"peer_id": mesage, "message": "Вы не ввели своё имя !", "random_id": random.randint(1, 2147483647)})
                                    connection.commit()
                                    connection.close()
                                else:
                                    q.execute(
                                        "UPDATE user_info SET Name='%s' WHERE User_ID = %s" % (user_name, id))
                                    vk.method("messages.send", {"peer_id": mesage, "message": "&#128203;Ваше имя успешно изменено на : " + user_name, "random_id": random.randint(1, 2147483647)})
                                    connection.commit()
                                    connection.close()



                    elif "перевод" in body.lower():
                        try:
                            connection = sql.connect("user.sqlite", check_same_thread=False)
                            q = connection.cursor()
                            q.execute("SELECT * FROM user_info WHERE User_ID = %s" % (id))
                            result = q.fetchall()
                            if len(result) == 0:
                                vk.method("messages.send", {"peer_id": mesage, "message": "Вы ещё не зарегистрировались ! Введите команду (начать)", "random_id": random.randint(1, 2147483647)})
                            else:
                                perevod_sum = str(body.lower()[10:])
                                perevod_id = str(body.lower()[7:10])
                                if perevod_id == "":
                                    vk.method("messages.send", {"peer_id": mesage, "message": "Вы не ввели id !", "random_id": random.randint(1, 2147483647)})
                                    connection.commit()
                                    connection.close()
                                elif perevod_sum == "":
                                    vk.method("messages.send", {"peer_id": mesage, "message": "Вы не ввели сумму перевода !", "random_id": random.randint(1, 2147483647)})
                                    connection.commit()
                                    connection.close()
                                elif int(perevod_sum) <= 0:
                                    vk.method("messages.send", {"peer_id": mesage, "message": "Перевод не может быть меньше или равен 0", "random_id": random.randint(1, 2147483647)})
                                    connection.commit()
                                    connection.close()
                                else:
                                    q = connection.cursor()
                                    q.execute("SELECT * FROM user_info WHERE id = %s" % (perevod_id))
                                    result = q.fetchall()
                                    if len(result) == 0:
                                        vk.method("messages.send", {"peer_id": mesage, "message": "Такого пользователя не существует !", "random_id": random.randint(1, 2147483647)})
                                        connection.commit()
                                        connection.close()
                                    else:
                                        user_name = result[0][1]
                                        q.execute("SELECT * FROM user_info WHERE User_ID = %s" % (id))
                                        result = q.fetchall()
                                        q.execute("UPDATE user_info SET Balance = '%s' WHERE User_ID = '%s'" % (result[0][3] - int(perevod_sum), id))
                                        q.execute("SELECT * FROM user_info WHERE User_ID = %s" % (id))
                                        result = q.fetchall()
                                        if result[0][3] <= 0:
                                            vk.method("messages.send", {"peer_id": mesage, "message": "&#128181;У вас недостаточно средств для перевода !", "random_id": random.randint(1, 2147483647)})
                                            q.execute("UPDATE user_info SET Balance = '%s' WHERE User_ID = '%s'" % (result[0][3] + int(perevod_sum), id))
                                            connection.commit()
                                            connection.close()
                                        else:
                                            q.execute("SELECT * FROM user_info WHERE id = %s" % (perevod_id))
                                            result = q.fetchall()
                                            q.execute("UPDATE user_info SET Balance = '%s' WHERE id = '%s'" % (result[0][3] + int(perevod_sum), perevod_id))
                                            vk.method("messages.send", {"peer_id": mesage, "message": "&#128184;Перевод совершён ! \n Сумма перевода: " + str(perevod_sum) + "\n Имя получателя: " + str(user_name), "random_id": random.randint(1, 2147483647)})
                                            connection.commit()
                                            connection.close()


                        except:
                            vk.method("messages.send", {"peer_id": mesage, "message": "id пользователя или сумма перевода введены не корректно !", "random_id": random.randint(1, 2147483647)})