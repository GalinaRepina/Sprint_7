import pytest
import requests

class TestOrderList:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/orders'
    
    def test_get_order_list(self):
        """Тест получения списка заказов"""
        response = requests.get(self.BASE_URL)
        
        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)