from flask_restful import Resource

from Common.Collections.DishesCollection import DishesCollection
from Common.Collections.MealsCollection import MealsCollection
from Common.Exceptions import ResourceNotFound
from Common.StatusCodes import RESPONSE_CODES


class Dish(Resource):
    """
    A Dish Resource.
        resource serves in routes '/dishes/<dish_id>' or '/dishes/<dish_name>'
    """
    _dishes_collection = DishesCollection()
    _meals_collection = MealsCollection()

    def get(self, dish_id: int = None, dish_name: str = None):
        """
        Handle GET request in form '/dishes/<dish_id>' or '/dishes/<dish_name>'

        Args:
        - dish_id: id of the dish in the collection
        - dish_name:  name of the dish in collection.

        Returns: dish date if exists in collection, else raise an appropriate exception.
        """
        try:
            return self._dishes_collection.fetch_record(dish_name, dish_id), \
                RESPONSE_CODES["Resource-Get-Successfully"]  # 200

        except ResourceNotFound:
            return RESPONSE_CODES["Resource-Does-Not-Exists"]  # -5, 404

    def delete(self, dish_id: int = None, dish_name: str = None):
        """
        Handle DELETE /dishes/{ID} /dishes/{name} deletes the ID of the dish and removes that dish from /dishes

        Args:
        - dish_id: id of the dish in the collection
        - dish_name:  name of the dish in collection.

        Returns: ID of the deleted dish if exists, else raise an appropriate exception.
        """
        try:
            dish_removed_recode = self._dishes_collection.delete_record(dish_name, dish_id)
            self._meals_collection.on_dish_deleted(dish_record=dish_removed_recode)

            return dish_removed_recode["ID"], RESPONSE_CODES["Resource-Deleted-Successfully"]  # 200

        except ResourceNotFound:
            return RESPONSE_CODES["Resource-Does-Not-Exists"]  # -5, 404
