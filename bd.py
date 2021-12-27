# Импортируем в программу модуль sqlite3
import sqlite3
#  Начинаем работу с базой данных. 
# Создаем таблицы
def connect():
    try:
        con = sqlite3.connect('shortlink.db')
# С помощью объекта соединения создается объект cursor, который позволяет выполнять SQLite-запросы
        cursor = con.cursor()
# Создаем таблицу users, в которой будут заключены все наши пользователи
        cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER,
            login TEXT NOT NULL,
            password TEXT NOT NULL,
            PRIMARY KEY(id AUTOINCREMENT));""")
        con.commit()
# Создаем таблицу links, в которой будут заключены наши ссылки
        cursor.execute("""CREATE TABLE IF NOT EXISTS links(
            id INTEGER,
            user_id INTEGER,
            psevdonim TEXT NOT NULL,
            link TEXT NOT NULL,
            status TEXT NOT NULL,
            PRIMARY KEY(id AUTOINCREMENT),
            FOREIGN KEY(user_id) REFERENCES users(id));""")
        con.commit()
# Выводим сообщение об ошибке  
    except sqlite3.Error:
        print("Ошибка. Невозможно создать базу данных.")
    finally:
        con.close()

# Проверяем наличие пользователя в базе данных. 
def login(login):
    try:
        print("Проверка")
        con = sqlite3.connect('shortlink.db')
        cursor = con.cursor()
        user = cursor.execute("""SELECT login FROM users WHERE login = ?""",(login,)).fetchone()
        if not user:
            print("Успешная регистрация")
            return 0
        else:
            print("Логин уже существует")
            return 1
   # Выводим сообщение об ошибке         
    except sqlite3.Error:
        print("Ошибка в авторизации")
    finally:
        con.close()

# Регистрация пользователя
def register(login, password):
    try:
        print("Регистрация")
        con = sqlite3.connect('shortlink.db')
        cursor = con.cursor()
        cursor.execute("""INSERT INTO users (login, password) VALUES(?, ?)""",(login, password,))
        con.commit()
        print("Вы зарегистрировались")
    except sqlite3.Error:
        print("Ошибка в регистрации")
        print(login)
    finally:
        con.close()

# Авторизация пользователя
def auth(login, password):
    try:
        print("Авторизация")
        con = sqlite3.connect('shortlink.db')
        cursor = con.cursor()
        user = cursor.execute("""SELECT * FROM users WHERE login = ? AND password = ?""",(login, password,)).fetchall()
        if len(user) == 0:
            print("Неверный логин или пароль")
            return 0
        else:
            print(user)
            print("Вы вошли в кабинет")
            return 1
    except sqlite3.Error:
        print("Ошибка в авторизации")
    finally:
        con.close()

# Ищем пользователя по логину
def getUser(login):
    try:
        con = sqlite3.connect('shortlink.db')
        cursor = con.cursor()
        res = cursor.execute("""SELECT * FROM users WHERE login = ? LIMIT 1""",(login,)).fetchone()
        if not res:
            print('Пользователь не найден')
            return False   
        return res
    except sqlite3.Error as e:
        print('Ошибка получения данных из базы данных' + str(e))
    return False

# Метод, который позволяет показывать ссылки по id
def getLink(id):
    try:
        print("Ваша ссылка")
        con = sqlite3.connect('shortlink.db')
        cursor = con.cursor()
        link = cursor.execute("""SELECT * FROM links WHERE id = ?""",(id,)).fetchone()
        con.commit()
        print(link)
        return link
    except sqlite3.Error:
        print("Ошибка при выводе ссылки")
    finally:
        con.close()


# Ищем пользователя по id
def getUser(user_id):
    try:
        con = sqlite3.connect('shortlink.db')
        cursor = con.cursor()
        res = cursor.execute("""SELECT * FROM users WHERE id = ? LIMIT 1""",(user_id,)).fetchone()
        if not res:
            print('Пользователь не найден')
            return False   
        return res
    except sqlite3.Error as e:
        print('Ошибка получения данных из базы данных' + str(e))
    return False

# Редактирование
def updateLink(psevdonim, status, id):
    try:
        print("Редактирование ссылки")
        con = sqlite3.connect('shortlink.db')
        cursor = con.cursor()
        link = cursor.execute("""UPDATE links SET psevdonim = ?, status = ? WHERE id = ?""",(psevdonim, status, id,)).fetchone()
        con.commit()
        print(link)
        return link
    except sqlite3.Error:
        print("Ошибка при редактировании ссылки")
    finally:
        con.close()

# Метод ,который позволяет сократить ссылку
def short(user_id, psevdonim, link, status):
    try:
        print("Идёт сокращение ссылки")
        con = sqlite3.connect('shortlink.db')
        cursor = con.cursor()
        cursor.execute("""INSERT INTO links (user_id, psevdonim, link, status) VALUES(?, ?, ?, ?)""",(user_id, psevdonim, link, status,))
        con.commit()
        print("Успешно сократили ссылку")
    except sqlite3.Error:
        print("Ошибка в сокращении")
    finally:
        con.close()

# Метод, который позволяет показывать приватные ссылки
def getLinkPrivate(user_id):
    try:
        print("Ваши приватные ссылки")
        con = sqlite3.connect('shortlink.db')
        cursor = con.cursor()
        links = cursor.execute("""SELECT * FROM links WHERE user_id = ?""",(user_id,)).fetchall()
        con.commit()
        print(links)
        return links
    except sqlite3.Error:
        print("Ошибка при выводе ссылок")
    finally:
        con.close()

# Метод, который позволяет показывать публичные ссылки
def getLinkPublic():
    try:
        print("Ваши публичные ссылки")
        con = sqlite3.connect('shortlink.db')
        cursor = con.cursor()
        links = cursor.execute("""SELECT * FROM links WHERE status = 'Публичная'""").fetchall()
        con.commit()
        print(links)
        return links
    except sqlite3.Error:
        print("Ошибка при выводе ссылок")
    finally:
        con.close()


# Метод, который позволяет показывать ссылки публичного доступа
def getLinkOBD():
    try:
        print("Ваши ссылки")
        con = sqlite3.connect('shortlink.db')
        cursor = con.cursor()
        links = cursor.execute("""SELECT * FROM links WHERE status = 'Общего доступа'""").fetchall()
        con.commit()
        print(links)
        return links
    except sqlite3.Error:
        print("Ошибка при выводе ссылок")
    finally:
        con.close()

# Метод, который позволяет удалить ссылки
def deleteLink(user_id,id):
    try:
        print("Удаление ссылки")
        con = sqlite3.connect('shortlink.db')
        cursor = con.cursor()
        cursor.execute("""DELETE FROM links WHERE user_id = ? AND id = ?""",(user_id,id,)).fetchone()
        con.commit()
    except sqlite3.Error:
        print("Ошибка при удалении")
    finally:
        con.close()





