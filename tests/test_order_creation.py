import pytest
import requests
import random

class TestOrderCreation:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/orders'
    
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_different_colors(self, color):
        """Тест создания заказа с разными цветами"""
        payload = {
            "firstName": f"Ivan{random.randint(1000, 9999)}",
            "lastName": f"Ivanov{random.randint(1000, 9999)}",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": f"+7 800 {random.randint(1000000, 9999999)}",
            "rentTime": 5,
            "deliveryDate": "2024-06-06",
            "comment": "Saske, come back to Konoha",
            "color": color
        }
        
        response = requests.post(self.BASE_URL, json=payload)
        
        assert response.status_code == 201
        assert "track" in response.json()
        
        # Правильное удаление заказа через параметры
        track = response.json()["track"]
        requests.put(f'{self.BASE_URL}/cancel', params={"track": track})