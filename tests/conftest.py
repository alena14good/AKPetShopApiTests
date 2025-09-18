from http.client import responses

import requests
import pytest

BASE_URL = 'http://5.181.109.28:9090/api/v3'

# Создание фикстуры для запроса по созданию питомца
@pytest.fixture(scope='function')
def create_pet():
    payload = {
        "id": 1,
        "name": "Buddy",
        "status": "available"
    }
    responses = requests.post(f'{BASE_URL}/pet', json=payload)

    assert responses.status_code == 200, "Другой статус код"
    return responses.json()