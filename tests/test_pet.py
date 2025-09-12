import allure
import requests

BASE_URL = 'http://5.181.109.28:9090/api/v3'
idNonexistentPet = 9999


@allure.feature("Pet")
class TestPet:
    @allure.title('Попытка удалить несуществующего питомца')
    @allure.description('Тест описания Allure. Сейчас будет проводиться запрос на удаление несуществующего питомца.')
    def test_delete_nonexistent_pet(self):
        with allure.step('Шаг 1 из кейса'):
            response = requests.delete(f'{BASE_URL}/pet/{idNonexistentPet}')

        with allure.step('Проверка статус кода'):
            assert response.status_code == 200, 'Статус код пришел не по ТЗ (не 200)'

        with allure.step('Проверка текста в ответе'):
            assert response.text == 'Pet deleted', 'Пришел другой текст в ответе'
