import pytest
import requests
import random
import string

def generate_random_string(length):
    """Генерирует случайную строку указанной длины"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

class TestCourierCreation:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/courier'
    
    def generate_unique_courier_data(self):
        """Генерирует уникальные данные для курьера"""
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)
        return login, password, first_name
    
    def test_create_courier_success(self):
        """Тест успешного создания курьера"""
        login, password, first_name = self.generate_unique_courier_data()
        
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        
        response = requests.post(self.BASE_URL, json=payload)
        
        assert response.status_code == 201
        assert response.json()["ok"] == True
        
        # Удаляем тестовые данные
        login_payload = {"login": login, "password": password}
        login_response = requests.post(f'{self.BASE_URL}/login', json=login_payload)
        courier_id = login_response.json()["id"]
        requests.delete(f'{self.BASE_URL}/{courier_id}')
    
    def test_create_duplicate_courier(self):
        """Тест создания дубликата курьера"""
        login, password, first_name = self.generate_unique_courier_data()
        
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        
        # Первое создание
        response1 = requests.post(self.BASE_URL, json=payload)
        assert response1.status_code == 201
        
        # Попытка создания дубликата
        response2 = requests.post(self.BASE_URL, json=payload)
        
        assert response2.status_code == 409
        assert "уже используется" in response2.json()["message"]
        
        # Очистка
        login_payload = {"login": login, "password": password}
        login_response = requests.post(f'{self.BASE_URL}/login', json=login_payload)
        courier_id = login_response.json()["id"]
        requests.delete(f'{self.BASE_URL}/{courier_id}')
    
    def test_create_courier_missing_login(self):
        """Тест создания курьера без логина"""
        payload = {
            "password": "password123",
            "firstName": "Ivan"
        }
        
        response = requests.post(self.BASE_URL, json=payload)
        
        assert response.status_code == 400
        assert "Недостаточно данных" in response.json()["message"]
    
    def test_create_courier_missing_password(self):
        """Тест создания курьера без пароля"""
        payload = {
            "login": "testlogin",
            "firstName": "Ivan"
        }
        
        response = requests.post(self.BASE_URL, json=payload)
        
        assert response.status_code == 400
        assert "Недостаточно данных" in response.json()["message"]