import pytest
import requests
import allure
from urls import Endpoints
from helpers.courier_helper import login_courier

class TestCourierLogin:

    @allure.title("Успешная авторизация курьера")
    @allure.description("Тест проверяет успешный логин курьера в систему")
    def test_login_success(self, setup_courier):
        """Тест успешного логина"""
        courier_data = setup_courier
        
        with allure.step("Выполнить авторизацию курьера"):
            payload = {"login": courier_data["login"], "password": courier_data["password"]}
            response = requests.post(Endpoints.COURIER_LOGIN, json=payload)
        
        with allure.step("Проверить успешную авторизацию"):
            assert response.status_code == 200
            assert "id" in response.json()

    @allure.title("Авторизация с неверным паролем")
    @allure.description("Тест проверяет обработку неверных учетных данных при авторизации")
    def test_login_wrong_password(self, setup_courier):
        """Тест логина с неправильным паролем"""
        courier_data = setup_courier
        
        with allure.step("Попытаться авторизоваться с неверным паролем"):
            payload = {"login": courier_data["login"], "password": "wrongpassword"}
            response = requests.post(Endpoints.COURIER_LOGIN, json=payload)
        
        with allure.step("Проверить ошибку авторизации"):
            assert response.status_code == 404
            assert "Учетная запись не найдена" in response.json()["message"]