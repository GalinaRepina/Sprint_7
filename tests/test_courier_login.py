# tests/test_courier_login.py
import pytest
import requests
import allure
from urls import Endpoints
from helpers.data_generator import generate_courier_data
from helpers.courier_helper import create_courier, login_courier, delete_courier

class TestCourierLogin:
    
    @allure.title("Тест успешного логина курьера")
    def test_login_success(self):
        """Тест успешного логина"""
        courier_data = generate_courier_data()
        
        # Создаем курьера
        create_courier(courier_data)
        
        # Логинимся
        payload = {"login": courier_data["login"], "password": courier_data["password"]}
        response = requests.post(Endpoints.COURIER_LOGIN, json=payload)
        
        assert response.status_code == 200
        assert "id" in response.json()
        
        # Пост-условие
        courier_id = response.json()["id"]
        delete_courier(courier_id)
    
    @allure.title("Тест логина с неправильным паролем")
    def test_login_wrong_password(self):
        """Тест логина с неправильным паролем"""
        courier_data = generate_courier_data()
        
        # Создаем курьера
        create_courier(courier_data)
        
        # Пытаемся логиниться с неправильным паролем
        payload = {"login": courier_data["login"], "password": "wrongpassword"}
        response = requests.post(Endpoints.COURIER_LOGIN, json=payload)
        
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json()["message"]
        
        # Пост-условие
        courier_id = login_courier(courier_data["login"], courier_data["password"])
        delete_courier(courier_id)