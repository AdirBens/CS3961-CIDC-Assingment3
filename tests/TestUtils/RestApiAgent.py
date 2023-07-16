import requests

from TestUtils import ConnectionController


def add_dish(name: str) -> requests.Response:
    dish = {"name": name}

    return ConnectionController.http_post("dishes", dish)


def add_meal(name: str, appetizer_id: int, main_id: int, dessert_id: int) -> requests.Response:
    meal = {
        "name": name,
        "appetizer": appetizer_id,
        "main": main_id,
        "dessert": dessert_id
    }

    return ConnectionController.http_post("meals", meal)


def get_dishes():
    return ConnectionController.http_get("dishes")


def get_dish_by_id(dish_id: int):
    return ConnectionController.http_get(f"dishes/{dish_id}")


def get_meals():
    return ConnectionController.http_get("meals")
