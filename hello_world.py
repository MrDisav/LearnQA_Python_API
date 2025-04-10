#print('Hello from Dmitriy')
from requests import get, post
from json.decoder import JSONDecodeError

url = 'https://playground.learnqa.ru/api/get_auth_cookie'
login = {
    'login' : 'secret_login',
    'password' : 'secret_pass'
}

response = post(url, data = login)
cookie_values = response.cookies.get('auth_cookie')
print(cookie_values)

payload = {
    'auth_cookie' : cookie_values
}
url_for_check_login = 'https://playground.learnqa.ru/api/check_auth_cookie'
check_login = post(url_for_check_login, cookies= payload)
print(check_login.text)
print(check_login.status_code)