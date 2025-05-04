from requests import Response
import json.decoder
from datetime import datetime

class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f'There is no cookie {cookie_name} in last response'
        return response.cookies[cookie_name]


    def get_header(self, response: Response, header_name):
        assert header_name in response.headers, f'There is no cookie {header_name} in last response'
        return response.headers[header_name]


    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f'Response isn`t in JSOn format. Rsponse text is {response.text}'
        assert name in response_as_dict, f'Response JSON doesn`t have key {name}'
        return response_as_dict[name]


    def prepare_registration_data(self, email = None, username = 'testusername'):
        if email is None:
            base_part = 'learnqa'
            domain = 'example.com'
            random_part = datetime.now().strftime('_%m_%d_%Y_%H_%M_%S') + f'{datetime.now().microsecond // 1000:03d}'
            email = f'{base_part}{random_part}@{domain}'
        return {
            'password': '123',
            'username': username,
            'firstName': 'testname',
            'lastName': 'testlastname',
            'email': email
        }
