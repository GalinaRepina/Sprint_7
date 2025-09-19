import pytest
import requests
import random
import string

def generate_random_string(length):
    """Генерирует случайную строку указанной длины"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

class TestCourierDeletion:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/courier'
    
    def generate_unique_courier_data(self):
        """Генерирует уникальные данные для курьера"""
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)
        return login, password, first_name
    
    def test_delete_courier_success(self):
        """Тест успешного удаления курьера"""
        login, password, first_name = self.generate_unique_courier_data()
        
        # Создаем курьера
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response = requests.post(self.BASE_URL, json=payload)
        assert response.status_code == 201
        
        # Логинимся для получения ID
        login_response = requests.post(f'{self.BASE_URL}/login', json={"login": login, "password": password})
        courier_id = login_response.json()["id"]
        
        # Удаляем курьера
        response = requests.delete(f'{self.BASE_URL}/{courier_id}')
        
        assert response.status_code == 200
        assert response.json()["ok"] == True
    
    def test_delete_nonexistent_courier(self):
        """Тест удаления несуществующего курьера"""
        response = requests.delete(f'{self.BASE_URL}/999999')
        
        assert response.status_code == 404
        assert "Курьера с таким id нет" in response.json()["message"]