import pytest
import requests
import allure
from urls import Endpoints
from helpers.courier_helper import login_courier, delete_courier

class TestCourierDeletion:

    @allure.title("Успешное удаление курьера")
    @allure.description("Тест проверяет корректное удаление курьера из системы")
    def test_delete_courier_success(self, setup_courier):
        """Тест успешного удаления курьера"""
        courier_data = setup_courier
        
        with allure.step("Получить ID курьера"):
            courier_id = login_courier(courier_data["login"], courier_data["password"])
            assert courier_id is not None
        
        with allure.step("Удалить курьера"):
            response = delete_courier(courier_id)
            assert response.status_code == 200
            assert response.json()["ok"] == True

    @allure.title("Удаление несуществующего курьера")
    @allure.description("Тест проверяет обработку попытки удаления несуществующего курьера")
    def test_delete_nonexistent_courier(self):
        """Тест удаления несуществующего курьера"""
        with allure.step("Попытаться удалить несуществующего курьера"):
            response = requests.delete(Endpoints.COURIER_DELETE.format(id=999999))
        
        with allure.step("Проверить ответ с ошибкой"):
            assert response.status_code == 404
            assert "Курьера с таким id нет" in response.json()["message"]