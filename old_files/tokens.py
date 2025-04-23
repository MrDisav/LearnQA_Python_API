import requests
import time
import pytest
from unittest.mock import ANY


URL_LONGTIME_JOB = "https://playground.learnqa.ru/ajax/api/longtime_job"


def test_start_job():
    response = requests.get(url=URL_LONGTIME_JOB)
    assert response.status_code == 200
    assert response.json()["token"]


def test_early_check_job():
    response = requests.get(url=URL_LONGTIME_JOB)
    params = {"token": response.json()["token"]}
    response = requests.get(url=URL_LONGTIME_JOB, params=params)
    assert response.json()["status"] == "Job is NOT ready"


def test_job_is_done():
    response = requests.get(url=URL_LONGTIME_JOB)
    params = {"token": response.json()["token"]}
    time.sleep(response.json()["seconds"])
    response = requests.get(url=URL_LONGTIME_JOB, params=params)
    data = response.json()
    assert data == {'status' : 'Job is ready',
                    'result' : ANY}



