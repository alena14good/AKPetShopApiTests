from http.client import responses

import allure
import requests

BASE_URL = 'http://5.181.109.28:9090/api/v3'
idNonexistentPet = 9999
dataNoneexistentPet = {"id": 9999, "name": "Non-existent Pet", "status": "available"}


@allure.feature("Pet")
class TestPet:
    @allure.title('Попытка удалить несуществующего питомца')
    @allure.description('Тест описания Allure. Сейчас будет проводиться запрос на удаление несуществующего питомца.')
    def test_delete_nonexistent_pet(self):
        with allure.step('Удаляем несуществующего питомца'):
            response = requests.delete(f'{BASE_URL}/pet/{idNonexistentPet}')

        with allure.step('Проверка статус кода'):
            assert response.status_code == 200, 'Статус код пришел не по ТЗ (не 200)'

        with allure.step('Проверка текста в ответе'):
            assert response.text == 'Pet deleted', 'Пришел другой текст в ответе'


    @allure.title('Попытка обновить несуществующего питомца')
    @allure.description('Данный тест берет данные несуществующего питомца и попытается их обновить')
    def test_update_nonexistent_pet(self):

        with allure.step('Отправка запроса на обновление несуществующего питомца'):
            response = requests.put(f'{BASE_URL}/pet', dataNoneexistentPet)

        with allure.step('Проверка статус кода'):
                assert response.status_code == 404, 'Статус кода не соответствует документации'

        with allure.step('Проверка текста ошибочного сообщения'):
                assert response.text == 'Pet not found', 'Пришел другой текст'

    @allure.title('Попытка получить информацию о несуществующем питомце')
    def test_get_info_about_nonexistent_pet(self):
        with allure.step('Отправляем запрос на получение информации'):
            response = requests.get(f'{BASE_URL}/pet/{idNonexistentPet}')

        with allure.step('Проверка статус кода'):
            assert response.status_code == 404, 'Статус кода не соответствует документации'

        with allure.step('Проверка текста в ответе'):
            assert response.text == 'Pet not found', 'Пришел другой текст'