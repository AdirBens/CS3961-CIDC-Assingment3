import json

from Common.Collections.DishesCollection import DishesCollection
from Common.Exceptions import ResourceNotFound, DishNotFound
from Utils.DataBase import DataBase
from Utils.Helpers import calc_round_sum


class MealsCollection(DataBase):
    """
    A Collection of Meals.
    Stores all meals Resources and provides encapsulation and interface to handle meals Resources.

    > An extension to DataBase class.
    [!] This is a singleton class, which can be shared among relevant classes
    """
    _instance = None
    _dishes_collection = DishesCollection()
    _DISH_MEAL_BINDS = {}

    def __init__(self):
        super().__init__()
        self._MEAL_RECORD_KEYS = ['name', 'appetizer', 'main', 'dessert', 'cal', 'sodium', 'sugar']
        self._DISH_TO_MEAL_BINDS = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MealsCollection, cls).__new__(cls)
        return cls._instance

    def insert_record(self, record, force_id: int | None = None) -> int:
        meal_record = self._assemble_meal(posted_meal=record)
        meal_id = super().insert_record(meal_record, force_id)
        self._bind_dish_to_meal(meal_id, meal_record)

        return meal_id

    def delete_record(self, record_name: str = None, record_id: int = None) -> json:
        deleted_meal = super().delete_record(record_name, record_id)
        self._unbind_dish_to_meal(deleted_meal)

        return deleted_meal

    def replace_record(self, record_id: int, new_record) -> int:
        self.delete_record(record_id=record_id)
        return self.insert_record(new_record, force_id=record_id)

    def on_dish_deleted(self, dish_record: json):
        dish_id = dish_record["ID"]
        binds_meals = self._DISH_TO_MEAL_BINDS.get(dish_id, [])

        for meal_id in binds_meals:
            self._STORAGE[meal_id]["cal"] -= dish_record["cal"]
            self._STORAGE[meal_id]["sodium"] -= dish_record["sodium"]
            self._STORAGE[meal_id]["sugar"] -= dish_record["sugar"]
            for meal_dish in ["appetizer", "main", "dessert"]:
                if self._STORAGE[meal_id][meal_dish] == dish_id:
                    self._STORAGE[meal_id][meal_dish] = None

    def _assemble_meal(self, posted_meal: json) -> json:
        dishes_ids = [posted_meal[dish] for dish in ["appetizer", "main", "dessert"]]

        try:
            dishes_data = [self._dishes_collection.fetch_record(record_id=dish_id)
                           for dish_id in dishes_ids]
        except ResourceNotFound:
            raise DishNotFound()

        posted_meal["cal"] = calc_round_sum("cal", dishes_data)
        posted_meal["sodium"] = calc_round_sum("sodium", dishes_data)
        posted_meal["sugar"] = calc_round_sum("sugar", dishes_data)

        return posted_meal

    def _bind_dish_to_meal(self, meal_id: int, meal_record: json):
        dishes_ids = [meal_record[dish] for dish in ["appetizer", "main", "dessert"]]

        for dish_id in dishes_ids:
            bind_list = self._DISH_TO_MEAL_BINDS.get(dish_id, [])
            bind_list.append(meal_id)
            self._DISH_TO_MEAL_BINDS[dish_id] = bind_list

    def _unbind_dish_to_meal(self, meal_record: json):
        dishes_ids = [meal_record[dish] for dish in ["appetizer", "main", "dessert"]]

        for dish_id in dishes_ids:
            bind_list = self._DISH_TO_MEAL_BINDS.get(dish_id, [])
            bind_list.remove(meal_record["ID"])
            self._DISH_TO_MEAL_BINDS[dish_id] = bind_list

