# tests/test_order_list.py
import pytest
import requests
import allure
from urls import Endpoints

class TestOrderList:
    
    @allure.title("Тест получения списка заказов")
    def test_get_order_list(self):
        """Тест получения списка заказов"""
        response = requests.get(Endpoints.ORDERS)
        
        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)