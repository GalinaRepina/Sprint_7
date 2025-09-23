# tests/test_order_acceptance.py
import pytest
import requests
import allure
from urls import Endpoints
from helpers.order_helper import get_order_id_by_track

class TestOrderAcceptance:
    
    @allure.title("Успешное принятие заказа курьером")
    @allure.description("Тест проверяет корректное принятие заказа курьером в систему")
    def test_accept_order_success(self, setup_courier, setup_order):
        """Тест успешного принятия заказа"""
        courier_data = setup_courier
        track = setup_order
        
        with allure.step("Получить ID курьера"):
            from helpers.courier_helper import login_courier
            courier_id = login_courier(courier_data["login"], courier_data["password"])
            assert courier_id is not None
        
        with allure.step("Получить ID заказа по track номеру"):
            order_id = get_order_id_by_track(track)
            assert order_id is not None
        
        with allure.step("Принять заказ курьером"):
            params = {"courierId": courier_id}
            response = requests.put(Endpoints.ORDER_ACCEPT.format(id=order_id), params=params)
        
        with allure.step("Проверить успешное принятие заказа"):
            assert response.status_code == 200
            assert response.json()["ok"] == True