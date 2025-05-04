from lib.BaseCase import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

class TestUserDelete(BaseCase):

    def test_user_2_delete(self):
        # LOGIN
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, 'x-csrf-token')

        # DELETE USER 2
        response_2 = response = MyRequests.delete(f"/user/2",
                                                  headers={"x-csrf-token": token},
                                                  cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response_2, 400)
        Assertions.assert_json_has_key(response_2, 'error', )
        Assertions.assert_json_value_by_name(response_2,
                                             'error',
                                             'Please, do not delete test users with ID 1, 2, 3, 4 or 5.',
                                             'User is deleted!')


    def test_delete_created_user(self):
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

        #DELETE USER
        response_2 = MyRequests.delete(f"/user/{user_id}",
                                                  headers={"x-csrf-token": token},
                                                  cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response_2, 200)

        #GET USER`S DELETE DATA
        response_3 = MyRequests.get(f"/user/{user_id}")
        Assertions.assert_code_status(response_3, 404)
        Assertions.response_has_text(response_3, 'User not found')


    def test_another_user_deletion(self):
        # REGISTRATION
        reg_data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=reg_data)

        email = reg_data['email']
        password = reg_data['password']

        # REGISTRATION ANOTHER USER TO DELETE
        reg_data_2 = self.prepare_registration_data()
        response_2 = MyRequests.post("/user/", data=reg_data_2)

        user_id = self.get_json_value(response_2, 'id')

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response_2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response_2, "auth_sid")
        token = self.get_header(response_2, 'x-csrf-token')

        #DELETION ANOTHER USER
        response_2 = MyRequests.delete(f"/user/{user_id}",
                                       headers={"x-csrf-token": token},
                                       cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response_2, 200)

        # GET USER`S DELETE DATA
        response_3 = MyRequests.get(f"/user/{user_id}")
        assert response_3.status_code != 404
        Assertions.assert_code_status(response_3, 200)
        Assertions.assert_json_has_key(response_3, 'username')
