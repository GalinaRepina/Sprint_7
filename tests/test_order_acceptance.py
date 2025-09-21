# tests/test_order_acceptance.py
import pytest
import requests
import allure
from urls import Endpoints
from helpers.data_generator import generate_courier_data, generate_order_data
from helpers.courier_helper import create_courier, login_courier, delete_courier
from helpers.order_helper import create_order, cancel_order, get_order_id_by_track

class TestOrderAcceptance:
    
    @allure.title("Тест успешного принятия заказа")
    def test_accept_order_success(self):
        """Тест успешного принятия заказа"""
        # Создаем курьера
        courier_data = generate_courier_data()
        create_response = create_courier(courier_data)
        assert create_response.status_code == 201
        
        courier_id = login_courier(courier_data["login"], courier_data["password"])
        assert courier_id is not None
        
        # Создаем заказ
        order_data = generate_order_data()
        order_response = create_order(order_data)
        assert order_response.status_code == 201
        
        track = order_response.json()["track"]
        
        # Получаем ID заказа
        order_id = get_order_id_by_track(track)
        assert order_id is not None
        
        # Принимаем заказ
        params = {"courierId": courier_id}
        response = requests.put(Endpoints.ORDER_ACCEPT.format(id=order_id), params=params)
        
        assert response.status_code == 200
        assert response.json()["ok"] == True
        
        # Пост-условия
        cancel_response = cancel_order(track)
        # Не проверяем статус отмены, так как заказ может быть уже принят
        delete_courier(courier_id)