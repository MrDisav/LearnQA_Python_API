
from lib.BaseCase import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import pytest


class TestUserRegister(BaseCase):
    def test_create_user_successful(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, 'id')


    def test_create_user_with_existing_email(self):
        used_email = 'vinkotov@example.com'
        data = self.prepare_registration_data(used_email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.text == f"Users with email '{used_email}' already exists",\
            f'unexpected response content - {response.text}'


    def test_incorrect_email_format(self):
        incorrect_email = 'vinkotovexample.com'
        data = self.prepare_registration_data(incorrect_email)

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.text == 'Invalid email format'


    def test_user_short_name(self):
        username = 's'
        data = self.prepare_registration_data(username=username)

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.text == "The value of 'username' field is too short"


    def test_user_long_name(self):
        username = ('lollollollollollollollollollollollollollollollollollollollollollollollollollollo'
                    'llollollollollollollollollollollollollollollollollollollollollollollollollollollol'
                    'lollollollollollollollollollollollollollollollollollollollollollollollollollollollollollol')
        data = self.prepare_registration_data(username=username)

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.text == "The value of 'username' field is too long"


    @pytest.mark.parametrize(
    "data",
    [
        {'username': 'testusername', 'firstName': 'testname', 'lastName': 'testlastname', 'email': 'some@example.com'},  # Нет password
        {'password': '123', 'firstName': 'testname', 'lastName': 'testlastname', 'email': 'some@example.com'},  # Нет username
        {'password': '123', 'username': 'testusername', 'lastName': 'testlastname', 'email': 'some@example.com'},  # Нет firstName
        {'password': '123', 'username': 'testusername', 'firstName': 'testname', 'email': 'some@example.com'},  # Нет lastName
        {'password': '123', 'username': 'testusername', 'firstName': 'testname', 'lastName': 'testlastname'},  # Нет email
    ]
    )
    def test_user_create_without_any_params(self, data):
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)

    #test without assertion on keys...