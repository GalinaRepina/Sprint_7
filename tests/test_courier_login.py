import pytest
import requests
from helpers.courier_helper import register_new_courier_and_return_login_password

class TestCourierLogin:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/courier'
    
    def test_login_success(self):
        """Тест успешного логина"""
        login, password, first_name = register_new_courier_and_return_login_password()
        
        # Создаем курьера
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        requests.post(self.BASE_URL, data=payload)
        
        # Логинимся
        login_payload = {"login": login, "password": password}
        response = requests.post(f'{self.BASE_URL}/login', data=login_payload)
        
        assert response.status_code == 200
        assert "id" in response.json()
        
        # Очистка
        courier_id = response.json()["id"]
        requests.delete(f'{self.BASE_URL}/{courier_id}')
    
    def test_login_wrong_password(self):
        """Тест логина с неправильным паролем"""
        login, password, first_name = register_new_courier_and_return_login_password()
        
        # Создаем курьера
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        requests.post(self.BASE_URL, data=payload)
        
        # Пытаемся логиниться с неправильным паролем
        login_payload = {"login": login, "password": "wrongpassword"}
        response = requests.post(f'{self.BASE_URL}/login', data=login_payload)
        
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json()["message"]
        
        # Очистка
        correct_login_payload = {"login": login, "password": password}
        login_response = requests.post(f'{self.BASE_URL}/login', data=correct_login_payload)
        courier_id = login_response.json()["id"]
        requests.delete(f'{self.BASE_URL}/{courier_id}')