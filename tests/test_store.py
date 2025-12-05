from http.client import responses

import allure
import requests
import pytest
import jsonschema
from attr.setters import validate

from .schemas.inventory_schema import INVENTORY_SCHEMA

BASE_URL = 'http://5.181.109.28:9090/api/v3'


@allure.feature("Store")
class TestStore:
    @allure.title("Размещение заказа (POST /store/order)")
    @allure.description("Отправка запроса на создание заказа")
    def test_create_order(self):
        payload = {
            "id": 14,
            "petId": 14122000,
            "quantity": 10,
            "status": "placed",
            "complete": True
        }
        with allure.step("Отправляем POST-запрос на создание заказа"):
            responses = requests.post(f'{BASE_URL}/store/order', json=payload)
            responses_json = responses.json()

        with allure.step('Проверка статус кода'):
            assert responses.status_code == 200, f'Ожидался статус 200, но пришел {responses.status_code}'

        with allure.step('Проверка, что ответ содержит данные заказа'):
            assert responses_json['id'] == payload['id'], f'Создалась запись не с {payload['id']}'
            assert responses_json['petId'] == payload['petId'], f'Создалась запись не с {payload['petId']}'
            assert responses_json['quantity'] == payload['quantity'], f'Создалась запись не с {payload['quantity']}'
            assert responses_json['status'] == payload['status'], f'Создалась запись не с {payload['status']}'
            assert responses_json['complete'] == payload['complete'], f'Создалась запись не с {payload['complete']}'

    @allure.title("Получение информации о заказе по ID (GET /store/order/{orderId})")
    @allure.description("Получение информации о заказе по айдишнику")
    def test_find_order_by_id(self, create_order):
        order_id = create_order['id']

        with allure.step("Отправляем GET-запрос на получение заказа по id"):
            responses = requests.get(f'{BASE_URL}/store/order/{order_id}')
            assert responses.status_code == 200, f'Ожидался статус 200, но пришел {responses.status_code}'

        with allure.step('Проверка, что ответ содержит данные заказа id'):
            assert responses.json()['id'] == order_id, f'Создалась запись не с {order_id}'

    @allure.title("Удаление заказа по ID (DELETE /store/order/{orderId})")
    @allure.description("Удаление заказа и проверка, что его не существует в базе данных")
    def test_delete_order_by_id(self, create_order):
        order_id = create_order['id']

        with allure.step("Отправляем DELETE-запрос на удаление заказа по id"):
            responses = requests.delete(f'{BASE_URL}/store/order/{order_id}')

        with allure.step("Проверка статус кода при удалении"):
            assert responses.status_code == 200, f'Ожидался статус 200, но пришел {responses.status_code}'

        with allure.step("Проверка, что такого заказа больше не существует в базе данных"):
            response = requests.get(f'{BASE_URL}/store/order/{order_id}')
            assert response.status_code == 404, f'Ожидался статус 404, но пришел {responses.status_code}'

    @allure.title("Попытка получить информацию о несуществующем заказе (GET /store/order/{orderId})")
    def test_get_info_about_nonexistent_order(self):
        id_nonexistent_order = 145555

        with allure.step("Отправляем GET-запрос на получение несуществующего заказа по id"):
            responses = requests.get(f'{BASE_URL}/store/order/{id_nonexistent_order}')
            assert responses.status_code == 404, f'Ожидался статус 404, но пришел {responses.status_code}'

    @allure.title("Получение инвентаря магазина (GET /store/inventory)")
    def test_get_inventory(self):
        with allure.step("Отправляем GET-запрос на получение инвентору магазина"):
            responses = requests.get(f'{BASE_URL}/store/inventory')
            assert responses.status_code == 200, f'Ожидался статус 200, но пришел {responses.status_code}'

            responses_json = responses.json()

        with allure.step("Проверка совпадению формата ответа"):
            jsonschema.validate(responses_json, INVENTORY_SCHEMA)

