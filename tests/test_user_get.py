from lib.BaseCase import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure



class TestUserGet(BaseCase):
    @allure.tag("smoke")
    def test_get_user_details_unauthorized(self):
        names = ['email, firstname', 'lastName']

        response = MyRequests.get("/user/2")
        Assertions.assert_json_has_key(response, 'username')
        Assertions.assert_json_has_no_key(response, names)
        print(response.text)


    def test_get_user_with_auth_as_same_user(self):
        names = ['username', 'email', 'firstName', 'lastName']

        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(
             f"/user/{user_id_from_auth_method}",
             headers={"x-csrf-token": token},
             cookies={"auth_sid": auth_sid}
         )
        Assertions.assert_json_has_keys(response2, names)


    def test_get_another_user_data(self):
        names = ['email', 'firstName', 'lastName']

        #Create user
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)
        data_to_login = {
            'email' : data['email'],
            'password': data['password']
        }

        #login created player
        response_2 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response_2, "auth_sid")
        token = self.get_header(response_2, "x-csrf-token")

        #Get another user information
        response_3 = MyRequests.get(
            f"/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_json_has_key(response_3, 'username')
        Assertions.assert_json_has_no_key(response_3, names)