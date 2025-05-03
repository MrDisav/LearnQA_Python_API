from lib.assertions import Assertions
from lib.BaseCase import BaseCase
from lib.my_requests import MyRequests


class TestUserEdit(BaseCase):
    #REGISTRATION
    def test_edit_just_created_user(self):
        reg_data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=reg_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, 'id')

        email = reg_data['email']
        firstName = reg_data['firstName']
        password = reg_data['password']
        user_id = self.get_json_value(response, 'id')


        #LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response_2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response_2, "auth_sid")
        token = self.get_header(response_2, 'x-csrf-token')


        #CHANGE_DATA
        new_name = 'ChangedName'

        response_3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response_3, 200)


        #GET_NE_DATA
        response_4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}, )

        Assertions.assert_json_value_by_name(
            response_4,
            'firstName',
            new_name,
            'Wrong new name of user')