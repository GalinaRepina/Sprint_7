# conftest.py
import pytest
import allure
from helpers.data_generator import generate_courier_data, generate_order_data
from helpers.courier_helper import create_courier, login_courier, delete_courier
from helpers.order_helper import create_order, cancel_order

@pytest.fixture
def setup_courier():
    """Фикстура для создания и удаления курьера"""
    courier_data = generate_courier_data()
    
    # Предусловие - создание курьера
    with allure.step("Создать тестового курьера"):
        create_response = create_courier(courier_data)
        assert create_response.status_code == 201
    
    yield courier_data  # Передаем данные в тест
    
    # Пост-условие - удаление курьера
    with allure.step("Удалить тестового курьера"):
        courier_id = login_courier(courier_data["login"], courier_data["password"])
        if courier_id:
            delete_response = delete_courier(courier_id)
            # Не проверяем статус, так как курьер мог быть удален ранее

@pytest.fixture  
def setup_order():
    """Фикстура для создания и отмены заказа"""
    order_data = generate_order_data()
    
    # Предусловие - создание заказа
    with allure.step("Создать тестовый заказ"):
        order_response = create_order(order_data)
        assert order_response.status_code == 201
        track = order_response.json()["track"]
    
    yield track  # Передаем track в тест
    
    # Пост-условие - отмена заказа
    with allure.step("Отменить тестовый заказ"):
        cancel_response = cancel_order(track)
        # Не проверяем статус, так как заказ мог быть отменен ранее