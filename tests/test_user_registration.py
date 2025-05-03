import requests
from lib.BaseCase import BaseCase
from lib.assertions import Assertions

class TestUserRegister(BaseCase):
    def test_create_user_with_existing_email(self):
        used_email = 'vinkotov@example.com'
        data = {
            'password': '123',
            'username': 'testusername',
            'firstName': 'testname',
            'lastName': 'testlastname',
            'email': used_email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        assert response.status_code == 400, f'Response status code is incorrect. Expect 400, got {response.status_code}'
        assert response.text == f"Users with email '{used_email}' already exists",\
            f'unexpected response content - {response.text}'
