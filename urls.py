# urls.py
BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1'

class Endpoints:
    COURIER = f'{BASE_URL}/courier'
    COURIER_LOGIN = f'{BASE_URL}/courier/login'
    COURIER_DELETE = f'{BASE_URL}/courier/{{id}}'
    ORDERS = f'{BASE_URL}/orders'
    ORDER_ACCEPT = f'{BASE_URL}/orders/accept/{{id}}'
    ORDER_CANCEL = f'{BASE_URL}/orders/cancel'
    ORDER_TRACK = f'{BASE_URL}/orders/track'