import pytest
from lib.BaseCase import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure



@allure.epic('Authorization cases')
class TestUserAuth(BaseCase):
    exclude_params = [
        ('no_cookie'),
        ('no_token')
    ]
    def setup_method(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response = MyRequests.post('/user/login', data=data)

        self.auth_sid = self.get_cookie(response, 'auth_sid')
        self.x_csrf_token = self.get_header(response, 'x-csrf-token')
        self.user_id = self.get_json_value(response, 'user_id')

    @allure.tag("smoke")
    @allure.description('This test successfully authorized user by email and password')
    def test_user_auth(self):
        response = MyRequests.get(
            '/user/auth',
            headers={'x-csrf-token': self.x_csrf_token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response,
            "user_id",
            self.user_id,
            'User id`s isn`t equal '
        )

    @allure.description('This test check authorization status with main params')
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):
        if condition == 'no_cookie':
            response = MyRequests.get(
                '/user/auth',
                headers={'x-csrf-token': self.x_csrf_token}
            )
        else:
            response = MyRequests.get(
                '/user/auth',
                cookies={"auth_sid": self.auth_sid}
            )

        Assertions.assert_json_value_by_name(
            response,
            'user_id',
            0,
            f'User authorized with {condition}'
        )
