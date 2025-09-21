# conftest.py
import pytest
from helpers.data_generator import generate_courier_data, generate_order_data
from helpers.courier_helper import create_courier, login_courier, delete_courier
from helpers.order_helper import create_order, cancel_order

@pytest.fixture
def setup_courier():
    """Фикстура для создания и удаления курьера"""
    courier_data = generate_courier_data()
    create_courier(courier_data)
    yield courier_data
    courier_id = login_courier(courier_data["login"], courier_data["password"])
    delete_courier(courier_id)

@pytest.fixture
def setup_order():
    """Фикстура для создания и отмены заказа"""
    order_data = generate_order_data()
    response = create_order(order_data)
    track = response.json()["track"]
    yield track
    cancel_order(track)