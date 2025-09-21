# tests/test_courier_deletion.py
import pytest
import requests
import allure
from urls import Endpoints
from helpers.data_generator import generate_courier_data
from helpers.courier_helper import create_courier, login_courier, delete_courier

class TestCourierDeletion:
    
    @allure.title("Тест успешного удаления курьера")
    def test_delete_courier_success(self):
        """Тест успешного удаления курьера"""
        courier_data = generate_courier_data()
        
        # Создаем курьера
        create_courier(courier_data)
        
        # Получаем ID курьера
        courier_id = login_courier(courier_data["login"], courier_data["password"])
        
        # Удаляем курьера
        response = delete_courier(courier_id)
        
        assert response.status_code == 200
        assert response.json()["ok"] == True
    
    @allure.title("Тест удаления несуществующего курьера")
    def test_delete_nonexistent_courier(self):
        """Тест удаления несуществующего курьера"""
        response = requests.delete(Endpoints.COURIER_DELETE.format(id=999999))
        
        assert response.status_code == 404
        assert "Курьера с таким id нет" in response.json()["message"]