# helpers/courier_helper.py
import requests
import allure
from urls import Endpoints

def create_courier(courier_data):
    """Создает курьера"""
    with allure.step("Создать курьера"):
        response = requests.post(Endpoints.COURIER, json=courier_data)
        return response  # Убираем raise_for_status()

def login_courier(login, password):
    """Логин курьера и возврат ID"""
    with allure.step("Залогинить курьера"):
        payload = {"login": login, "password": password}
        response = requests.post(Endpoints.COURIER_LOGIN, json=payload)
        if response.status_code == 200:
            return response.json()["id"]
        return None  # Возвращаем None если логин не удался

def delete_courier(courier_id):
    """Удаляет курьера по ID"""
    with allure.step("Удалить курьера"):
        response = requests.delete(Endpoints.COURIER_DELETE.format(id=courier_id))
        return response  # Убираем raise_for_status()