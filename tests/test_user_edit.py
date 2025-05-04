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


        #GET_NEW_DATA
        response_4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}, )

        Assertions.assert_json_value_by_name(
            response_4,
            'firstName',
            new_name,
            'Wrong new name of user')


    def test_edit_user_data_unauthorized(self):
        #CREATE USER
        reg_data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=reg_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, 'id')

        email = reg_data['email']
        firstName = reg_data['firstName']
        password = reg_data['password']
        user_id = self.get_json_value(response, 'id')

        #CHANGING DATA
        new_name = 'ChangedName'

        response_2 = MyRequests.put(
            f"/user/{user_id}",
            data={"firstName": new_name}
        )
        Assertions.assert_code_status(response_2, 400)
        Assertions.assert_json_has_key(response_2, 'error')
        Assertions.assert_json_value_by_name(response_2,
                                             "error",
                                             'Auth token not supplied',
                                             'There is auth_token in json')



    def test_edit_another_user_data(self):
        # REGISTRATION
        reg_data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=reg_data)

        email = reg_data['email']
        password = reg_data['password']

        # REGISTRATION ANOTHER USER TO CHANGE
        reg_data_2 = self.prepare_registration_data()
        response_2 = MyRequests.post("/user/", data=reg_data_2)

        second_email = reg_data_2['email']
        second_password = reg_data_2['password']
        user_id = self.get_json_value(response_2, 'id')


        # LOGIN FIRST USER
        login_data = {
            'email': email,
            'password': password
        }
        response_2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response_2, "auth_sid")
        token = self.get_header(response_2, 'x-csrf-token')

        # CHANGE_DATA
        new_name = 'sometestname111'

        response_3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        #LOGIN TO ASSERT CHANGES
        login_data = {
            'email': second_email,
            'password': second_password
        }
        response_2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response_2, "auth_sid")
        token = self.get_header(response_2, 'x-csrf-token')

        #GET_NEW_DATA
        response_4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}, )

        assert response_4.json()["firstName"] != "sometestname111"
        Assertions.assert_json_value_by_name(response_4,
                                             'firstName',
                                             reg_data_2['firstName'],
                                             "There is another name")


    def test_user_change_incorrect_email(self):
        # REGISTRATION
        reg_data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=reg_data)

        email = reg_data['email']
        password = reg_data['password']
        user_id = self.get_json_value(response, 'id')


        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response_2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response_2, "auth_sid")
        token = self.get_header(response_2, 'x-csrf-token')

        # CHANGE_DATA
        new_email = 'sometest.com'

        response_3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )

        Assertions.assert_code_status(response_3, 400)
        Assertions.assert_json_has_key(response_3, 'error')
        Assertions.assert_json_value_by_name(response_3,
                                             'error',
                                             'Invalid email format',
                                             "Email was saved!")


    def test_user_change_short_first_name(self):
        # REGISTRATION
        reg_data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=reg_data)

        email = reg_data['email']
        password = reg_data['password']
        user_id = self.get_json_value(response, 'id')

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response_2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response_2, "auth_sid")
        token = self.get_header(response_2, 'x-csrf-token')

        # CHANGE_DATA
        new_name = 'A'

        response_3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response_3, 400)
        Assertions.assert_json_has_key(response_3, 'error')
        Assertions.assert_json_value_by_name(response_3,
                                             'error',
                                             'The value for field `firstName` is too short',
                                             "Name was saved!")