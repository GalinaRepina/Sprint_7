# tests/test_courier_creation.py
import pytest
import requests
import allure
from urls import Endpoints
from helpers.data_generator import generate_courier_data
from helpers.courier_helper import create_courier

class TestCourierCreation:

    @allure.title("Успешное создание курьера")
    @allure.description("Тест проверяет успешное создание нового курьера в системе")
    def test_create_courier_success(self, setup_courier):
        """Тест успешного создания курьера"""
        # Курьер уже создан фикстурой setup_courier
        # Проверяем что данные валидны
        courier_data = setup_courier
        assert "login" in courier_data
        assert "password" in courier_data
        assert "firstName" in courier_data
        # Фикстура автоматически выполнит пост-условие (удаление курьера)

    @allure.title("Создание дубликата курьера")
    @allure.description("Тест проверяет обработку попытки создания курьера с существующим логином")
    def test_create_duplicate_courier(self, setup_courier):
        """Тест создания дубликата курьера"""
        courier_data = setup_courier
        
        # Попытка создания дубликата
        with allure.step("Попытаться создать дубликат курьера"):
            response = create_courier(courier_data)
        
        assert response.status_code == 409
        assert "уже используется" in response.json()["message"]
        # Фикстура автоматически выполнит пост-условие

    @pytest.mark.parametrize("payload,expected_message", [
        ({"password": "password123", "firstName": "Ivan"}, "Недостаточно данных"),
        ({"login": "testlogin", "firstName": "Ivan"}, "Недостаточно данных")
    ])
    @allure.title("Создание курьера с недостаточными данными: {expected_message}")
    @allure.description("Тест проверяет валидацию обязательных полей при создании курьера")
    def test_create_courier_missing_data(self, payload, expected_message):
        """Тест создания курьера с недостаточными данными"""
        with allure.step("Отправить запрос с недостаточными данными"):
            response = requests.post(Endpoints.COURIER, json=payload)
        
        with allure.step("Проверить ответ с ошибкой"):
            assert response.status_code == 400
            assert expected_message in response.json()["message"]