import requests
import pytest
from datetime import datetime, timezone


@pytest.mark.parametrize('header_name, expected_value',[
    ('Content-Type', 'application/json'),
    ('Content-Length', '15'),
    ('Connection', 'keep-alive'),
    ('Keep-Alive', 'timeout=10'),
    ('Server', 'Apache'),
    ('x-secret-homework-header', 'Some secret value'),
    ('Cache-Control', 'max-age=0')
])

def test_check_headers_value(header_name, expected_value):
    response = requests.get(url='https://playground.learnqa.ru/api/homework_header')
    print(response.headers)
    assert header_name in response.headers
    assert response.headers.get(header_name) == expected_value


