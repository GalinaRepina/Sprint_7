# tests/test_order_creation.py
import pytest
import requests
import allure
from urls import Endpoints
from helpers.data_generator import generate_order_data
from helpers.order_helper import create_order

class TestOrderCreation:
    
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"], 
        ["BLACK", "GREY"],
        []
    ])
    @allure.title("Создание заказа с цветами: {color}")
    @allure.description("Тест проверяет создание заказов с различными комбинациями цветов самокатов")
    def test_create_order_with_different_colors(self, color):
        """Тест создания заказа с разными цветами"""
        with allure.step("Сгенерировать данные заказа с указанным цветом"):
            order_data = generate_order_data(color)
        
        with allure.step("Создать заказ"):
            response = create_order(order_data)
        
        with allure.step("Проверить успешное создание заказа"):
            assert response.status_code == 201
            assert "track" in response.json()
        
        with allure.step("Отменить тестовый заказ"):
            from helpers.order_helper import cancel_order
            track = response.json()["track"]
            cancel_order(track)