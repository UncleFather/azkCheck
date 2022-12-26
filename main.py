import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime as dt
from initials import azk_username, azk_password, azk_address


# Процедура проверки доступности хоста пингом
def ping_check(hostname):
    # Проверяем доступность с 4-х попыток, время задержки 4000 мс
    response = os.system("ping -n 4 -w 4000 " + hostname)
    # Если ответ получен, возвращаем «True», иначе - «False»
    return True if response == 0 else False


# Инициализируем драйвер Google Chrome
driver = webdriver.Chrome("chromedriver")
# Формируем начало сообщения для записи в файл журнала
message = f'{"".join(["-" for i in range(60)])}\n{dt.now():%d.%m.%Y %H:%M:%S}\n'
# Объявляем переменную для записи продолжения сообщения
result = ''

# Пытаемся открыть страницу системы АЦК-Финансы, войти и выйти
try:
    # Устанавливаем размер окна браузера
    driver.set_window_size(1561, 1060)
    # Переходим на страницу входа на сайт
    driver.get(f'https://{azk_address}/azk/login.jsp')

    # Ждем 10 секунд
    sleep(10)
    # Парсим страничку входа. Находим поле для ввода имени пользователя и записываем в него имя
    driver.find_element(By.ID, "re_Login_userNameField-inputEl").send_keys(azk_username)
    # Находим поле для ввода пароля и записываем в него пароль
    driver.find_element(By.ID, "re_Login_passwordField-inputEl").send_keys(azk_password)
    # Находим кнопку отправки и нажимаем ее
    driver.find_element(By.ID, "re_Login_Submit_Button-btnInnerEl").click()

    # Ждем 2 секунды
    sleep(2)
    try:
        # Пытаемся найти кнопку, подтверждающую повторный вход пользователя и нажать "Да"
        driver.find_element(By.ID, "button-1023-btnEl").click()
    except Exception:
        pass

    # Ждем 30 секунд
    sleep(30)
    try:
        # Пытаемся найти кнопку, закрывающую сообщение о скором истечении ЭЦП
        driver.find_element(By.ID, "button-1105-btnEl").click()
    except Exception:
        pass

    # Ждем 2 секунды
    sleep(2)
    # Находим кнопку выхода и нажимаем ее
    driver.find_element(By.ID, "button-1090-btnEl").click()
    # Ждем 2 секунды
    sleep(2)
    # Находим кнопку подтверждения выхода и нажимаем ее
    driver.find_element(By.ID, "button-1127-btnEl").click()

    # Ждем 3 секунды
    sleep(3)
    # Если все прошло успешно, формируем вторую часть сообщения
    result = 'Система «АЦК-Финансы» доступна\n'

# При появлении любой ошибки обрабатываем ее
except Exception as my_error:
    # Выполняем пинг до сервера Барса и формируем вторую часть сообщения
    result = f'Проблемы с системой «АЦК-Финансы» (Проверка пингом прошла {"" if ping_check(azk_address) else "без"}успешно):\n{my_error.__class__.__name__}\n'

# Закрываем окно экземпляра браузера
driver.close()

# Открываем файл для записи результатов проверки
handler = open('azk_log.txt', 'a', encoding='utf8')
# Записываем сообщение в файл
handler.write(f'{message}{result}')
# Закрываем файл
handler.close()
