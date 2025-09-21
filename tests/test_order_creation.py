# tests/test_order_creation.py
import pytest
import requests
import allure
from urls import Endpoints
from helpers.data_generator import generate_order_data
from helpers.order_helper import create_order, cancel_order

class TestOrderCreation:
    
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    @allure.title("Тест создания заказа с разными цветами: {color}")
    def test_create_order_with_different_colors(self, color):
        """Тест создания заказа с разными цветами"""
        order_data = generate_order_data(color)
        
        response = create_order(order_data)
        
        assert response.status_code == 201
        assert "track" in response.json()
        
        # Пост-условие
        track = response.json()["track"]
        cancel_order(track)