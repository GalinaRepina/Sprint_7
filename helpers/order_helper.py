# helpers/order_helper.py
import requests
import allure
from urls import Endpoints

def create_order(order_data):
    """Создает заказ"""
    with allure.step("Создать заказ"):
        response = requests.post(Endpoints.ORDERS, json=order_data)
        return response  # Убираем raise_for_status()

def cancel_order(track):
    """Отменяет заказ"""
    with allure.step("Отменить заказ"):
        response = requests.put(Endpoints.ORDER_CANCEL, params={"track": track})
        return response  # Убираем raise_for_status()

def get_order_id_by_track(track):
    """Получает ID заказа по track"""
    with allure.step("Получить ID заказа по track"):
        response = requests.get(Endpoints.ORDER_TRACK, params={"t": track})
        if response.status_code == 200:
            return response.json()["order"]["id"]
        return None  # Возвращаем None если заказ не найден