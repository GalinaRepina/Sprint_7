# tests/test_courier_creation.py
import pytest
import requests
import allure
from urls import Endpoints
from helpers.data_generator import generate_courier_data
from helpers.courier_helper import create_courier, login_courier, delete_courier

class TestCourierCreation:
    
    @allure.title("Тест успешного создания курьера")
    def test_create_courier_success(self):
        """Тест успешного создания курьера"""
        courier_data = generate_courier_data()
        
        response = create_courier(courier_data)
        
        assert response.status_code == 201
        assert response.json()["ok"] == True
        
        # Пост-условие
        courier_id = login_courier(courier_data["login"], courier_data["password"])
        if courier_id:
            delete_courier(courier_id)
    
    @allure.title("Тест создания дубликата курьера")
    def test_create_duplicate_courier(self):
        """Тест создания дубликата курьера"""
        courier_data = generate_courier_data()
        
        # Первое создание
        response1 = create_courier(courier_data)
        assert response1.status_code == 201
        
        # Попытка создания дубликата
        response2 = create_courier(courier_data)
        
        assert response2.status_code == 409
        assert "уже используется" in response2.json()["message"]
        
        # Пост-условие
        courier_id = login_courier(courier_data["login"], courier_data["password"])
        if courier_id:
            delete_courier(courier_id)

    @pytest.mark.parametrize("payload,expected_message", [
        ({"password": "password123", "firstName": "Ivan"}, "Недостаточно данных"),
        ({"login": "testlogin", "firstName": "Ivan"}, "Недостаточно данных")
    ])
    @allure.title("Тест создания курьера с недостаточными данными")
    def test_create_courier_missing_data(self, payload, expected_message):
        """Тест создания курьера с недостаточными данными"""
        response = requests.post(Endpoints.COURIER, json=payload)
        
        assert response.status_code == 400
        assert expected_message in response.json()["message"]