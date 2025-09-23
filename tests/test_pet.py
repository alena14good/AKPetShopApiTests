from http.client import responses

import jsonschema
import pytest

from .schemas.pet_schema import PET_SCHEMA
import allure
import requests

BASE_URL = 'http://5.181.109.28:9090/api/v3'
id_nonexistent_Pet = 9999


@allure.feature("Pet")
class TestPet:
    @allure.title('Попытка удалить несуществующего питомца')
    @allure.description('Тест описания Allure. Сейчас будет проводиться запрос на удаление несуществующего питомца.')
    def test_delete_nonexistent_pet(self):
        with allure.step('Удаляем несуществующего питомца'):
            response = requests.delete(f'{BASE_URL}/pet/{id_nonexistent_Pet}')

        with allure.step('Проверка статус кода'):
            assert response.status_code == 200, 'Статус код пришел не по ТЗ (не 200)'

        with allure.step('Проверка текста в ответе'):
            assert response.text == 'Pet deleted', 'Пришел другой текст в ответе'

    @allure.title('Попытка обновить несуществующего питомца')
    @allure.description('Данный тест берет данные несуществующего питомца и попытается их обновить')
    def test_update_nonexistent_pet(self):
        with allure.step('Отправка запроса на обновление несуществующего питомца'):
            data_noneexistent_pet = {"id": 9999, "name": "Non-existent Pet", "status": "available"}
            response = requests.put(f'{BASE_URL}/pet', data_noneexistent_pet)

        with allure.step('Проверка статус кода'):
            assert response.status_code == 404, 'Статус кода не соответствует документации'

        with allure.step('Проверка текста ошибочного сообщения'):
            assert response.text == 'Pet not found', 'Пришел другой текст'

    @allure.title('Попытка получить информацию о несуществующем питомце')
    def test_get_info_about_nonexistent_pet(self):
        with allure.step('Отправляем запрос на получение информации'):
            response = requests.get(f'{BASE_URL}/pet/{id_nonexistent_Pet}')

        with allure.step('Проверка статус кода'):
            assert response.status_code == 404, 'Статус кода не соответствует документации'

        with allure.step('Проверка текста в ответе'):
            assert response.text == 'Pet not found', 'Пришел другой текст'

    @allure.title('Добавление нового питомца c полными данными (POST /pet)')
    def test_create_new_pet_with_full_data(self):
        with allure.step('Подготовка тестовых данных'):
            payload = {
                "id": 10,
                "name": "Pupy",
                "category": {
                    "id": 1,
                    "name": "Dogs"
                },
                "photoUrls": ["string"],
                "tags": [
                    {
                        "id": 0,
                        "name": "string"
                    }
                ],
                "status": "available"
            }

        with allure.step('Отправка POST-запроса с тестовыми данными'):
            response = requests.post(f'{BASE_URL}/pet', json=payload)
            response_json = response.json()  # вывели результат функции в переменную, чтобы в последних ассертах вызывать переменную, а не функцию

        with allure.step('Проверка статус кода'):
            assert response.status_code == 200, 'Запрос прошел с другим статус кодом'

        with allure.step('Проверка валидации json-схемы'):
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step('Проверка, что создалась запись с корректными данными'):
            assert response_json['id'] == payload['id'], f'Создалась запись не с {payload['id']}'
            assert response_json['name'] == payload['name'], f'Создалась запись не с {payload['name']}'
            assert response_json['category']['id'] == payload['category'][
                'id'], f'Создалась запись не с {payload['category']['id']}'
            assert response_json['category']['name'] == payload['category'][
                'name'], f'Создалась запись не с {payload['category']['name']}'
            assert response_json['photoUrls'] == payload['photoUrls'], f'Создалась запись не с {payload['photoUrls']}'
            assert response_json['tags'][0]['id'] == payload['tags'][0][
                'id'], f'Создалась запись не с {payload['tags'][0]['id']}'
            assert response_json['tags'][0]['name'] == payload['tags'][0][
                'name'], f'Создалась запись не с {payload['tags'][0]['name']}'
            assert response_json['status'] == payload['status'], f'Создалась запись не с {payload['status']}'

    @allure.title("Обновление информации о питомце (PUT /pet)")
    def test_update_info_about_pet(self, create_pet):
        with allure.step('Подготовка тестовых данных'):
            pet_id = create_pet["id"]
            payoload = {
                "id": pet_id,
                "name": "Alens",
                "status": "sold"
            }
        with allure.step('Отправка запроса на обновление данных'):
            response = requests.put(f'{BASE_URL}/pet', json=payoload)
            assert response.status_code == 200, "Другой статус код"

        with allure.step('Проверка, что создалась запись с новыми данными'):
            response_json = response.json()
            assert response_json["id"] == payoload["id"], f'Создалась некорректная запись'
            assert response_json["name"] == payoload["name"], f'Создалась некорректная запись'
            assert response_json["status"] == payoload["status"], f'Создалась некорректная запись'

    @allure.title('Удаление питомца по ID (DELETE /pet/{petId})')
    def test_delete_pet_with_ID(self, create_pet):
        with allure.step('Подготовка тестовых данных'):
            pet_id = create_pet["id"]

        with allure.step('Отправка запроса на удаление питомца данных'):
            response = requests.delete(f'{BASE_URL}/pet/{pet_id}')
            assert response.status_code == 200, "Другой статус код"

        with allure.step('Проверка, что питомец удален и его нет в бд'):
            response = requests.get(f'{BASE_URL}/pet/{pet_id}')
            assert response.status_code == 404, "Другой статус код"

    @allure.title('Получение списка питомцев по статусу positive (GET /pet/findByStatus)')
    @pytest.mark.parametrize(
        "status, expected_status_code",
        [
            ("available", 200),
            ("pending", 200),
            ("sold", 200)
        ]
    )
    def test_get_pets_by_status_positive(self, status, expected_status_code):
        with allure.step(f'Отправка GET-запроса со статусом {status}'):
            response = requests.get(f'{BASE_URL}/pet/findByStatus', params={"status": status})

        with allure.step('Проверка статус кода'):
            assert response.status_code == expected_status_code, 'Статус код другой'
            assert isinstance(response.json(), list), "Ответ не является списком"

    @allure.title('Получение списка питомцев по статусу negative (GET /pet/findByStatus)')
    @pytest.mark.parametrize(
        "status, expected_status_code",
        [
            ("nonexistance_status", 400),
            (" ", 400)
        ]
    )
    def test_get_pets_by_status_negative(self, status, expected_status_code):
        with allure.step(f'Отправка GET-запроса со статусом {status}'):
            response = requests.get(f'{BASE_URL}/pet/findByStatus', params={"status": status})

        with allure.step('Проверка статус кода'):
            assert response.status_code == expected_status_code, 'Статус код другой'


