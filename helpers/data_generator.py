import random
import string

def generate_random_string(length=10):
    """Генерирует случайную строку указанной длины"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def generate_courier_data():
    """Генерирует данные для курьера"""
    return {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10)
    }

def generate_order_data(color=None):
    """Генерирует данные для заказа"""
    if color is None:
        color = ["BLACK"]
    
    return {
        "firstName": f"Test{random.randint(1000, 9999)}",
        "lastName": f"User{random.randint(1000, 9999)}",
        "address": "Test address",
        "metroStation": random.randint(1, 10),
        "phone": f"+7 800 {random.randint(1000000, 9999999)}",
        "rentTime": random.randint(1, 10),
        "deliveryDate": "2024-06-06",
        "comment": "Test order",
        "color": color
    }