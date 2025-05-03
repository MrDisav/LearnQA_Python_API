
from lib.BaseCase import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


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
