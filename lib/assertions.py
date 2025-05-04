from requests import Response
import json.decoder

class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f'Not a JSON. Response text is {response.text}'
        assert name in response_as_dict, f'Response JSON doesn`t have a key {name}'
        assert response_as_dict[name] == expected_value, error_message


    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f'Not a JSON. Response text is {response.text}'
        assert name in response_as_dict, f'Response JSON doesn`t have a key {name}'


    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, (f'Unexpected status code. '
                                                              f'Expect {expected_status_code}, '
                                                              f'but got {response.status_code}')


    @staticmethod
    def assert_json_has_no_key(response: Response, name: list):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f'Not a JSON. Response text is {response.text}'
        for every_elem in name:
            assert every_elem not in response_as_dict, f'Response JSON have a key {every_elem}'


    @staticmethod
    def assert_json_has_keys(response: Response, name: list):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f'Not a JSON. Response text is {response.text}'
        for every_elem in name:
            assert every_elem in response_as_dict, f'Response JSON doesn`t have a key {every_elem}'