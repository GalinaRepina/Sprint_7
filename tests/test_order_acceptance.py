import pytest
import requests
import random
import string

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

class TestOrderAcceptance:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/orders'
    COURIER_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/courier'
    
    def test_accept_order_success(self):
        """Тест успешного принятия заказа"""
        # Создаем уникального курьера
        login = generate_random_string(10)
        password = generate_random_string(10)
        courier_payload = {
            "login": login,
            "password": password,
            "firstName": generate_random_string(8)
        }
        courier_response = requests.post(self.COURIER_URL, json=courier_payload)
        assert courier_response.status_code == 201
        
        # Логинимся для получения ID курьера
        login_response = requests.post(f'{self.COURIER_URL}/login', json={"login": login, "password": password})
        assert login_response.status_code == 200
        courier_id = login_response.json()["id"]
        
        # Создаем заказ
        order_payload = {
            "firstName": f"Test{random.randint(1000, 9999)}",
            "lastName": f"User{random.randint(1000, 9999)}",
            "address": "Test address",
            "metroStation": 1,
            "phone": f"+7 800 {random.randint(1000000, 9999999)}",
            "rentTime": 1,
            "deliveryDate": "2024-06-06",
            "comment": "Test order",
            "color": ["BLACK"]
        }
        order_response = requests.post(self.BASE_URL, json=order_payload)
        assert order_response.status_code == 201
        
        # Получаем track заказа
        track = order_response.json()["track"]
        
        # Получаем ID заказа через endpoint получения заказа по track
        track_response = requests.get(f'{self.BASE_URL}/track', params={"t": track})
        assert track_response.status_code == 200
        order_id = track_response.json()["order"]["id"]
        
        # Правильное принятие заказа через параметры
        params = {"courierId": courier_id}
        response = requests.put(f'{self.BASE_URL}/accept/{order_id}', params=params)
        
        assert response.status_code == 200
        assert response.json()["ok"] == True
        
        # Очистка
        requests.put(f'{self.BASE_URL}/cancel', params={"track": track})
        requests.delete(f'{self.COURIER_URL}/{courier_id}')