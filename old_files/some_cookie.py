import requests
import pytest

def test_check_cookie_value():
    response = requests.get(url='https://playground.learnqa.ru/api/homework_cookie')
    print(response.cookies)
    assert 'HomeWork' in response.cookies, 'There is no filed "HomeWork" in cookies'
    assert response.cookies.get('HomeWork') == 'hw_value', 'Value isn`t equal to "hw_value"'
