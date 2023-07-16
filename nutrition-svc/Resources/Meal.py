from flask import request
from flask_restful import Resource, reqparse

from Common.Collections.DishesCollection import DishesCollection
from Common.Collections.MealsCollection import MealsCollection
from Common.Exceptions import ResourceNotFound, MissingBodyParameter, InvalidBodyParameter, DishNotFound
from Common.StatusCodes import RESPONSE_CODES
from Utils.Helpers import arg_parser


class Meal(Resource):
    _PUT_BODY_PARAMS = {'name': str, 'appetizer': int,
                        'main': int, 'dessert': int}
    _meals_collection = MealsCollection()
    _dishes_collection = DishesCollection()

    def get(self, id: int = None, name: str = None):
        """
        Handle GET request in form '/meals/<meal_id>' or '/meals/<meal_name>'

        Args:
        - id: id of the meal in the collection
        - name:  name of the meal in collection.

        Returns: meal date if exists in collection, else raise an appropriate exception.
        """
        try:
            return self._meals_collection.fetch_record(name, id), \
                RESPONSE_CODES["Resource-Get-Successfully"]  # 200

        except ResourceNotFound:
            return RESPONSE_CODES["Resource-Does-Not-Exists"]  # -5, 404

    def put(self, id: int):
        """
        Handle PUT /meals/{ID} request: Use to Modify an Existing dish.

        Args:
        - as query parameter = id of the modifying dish
        - in message body = json contains meal name, appetizer, main, dessert.

        Returns:
        - if successfully, returns meal ID (positive integer) and code 200
        - could also return non-positive ID with:
            * 0 if request content-type is not application/json (status code 415)
            * -1 if one of the required parameters was not given or not specified correctly (status code 422)
            * -2 if a meal of the given name already exists (status code 422)
            * -6 if one of the sents dish IDs does not exist (status code 422)
        """
        if request.headers.get('Content-Type', '') != 'application/json':
            return RESPONSE_CODES["Content-Type-Exception"]  # 0, 415

        parser = reqparse.RequestParser()
        try:
            args = arg_parser(parser, self._PUT_BODY_PARAMS)

        except MissingBodyParameter or InvalidBodyParameter:
            return RESPONSE_CODES["Invalid-Body-Parameters"]  # -1, 422

        try:
            posted_meal = {"name": args["name"],
                           "appetizer": args["appetizer"],
                           "main": args["main"],
                           "dessert": args["dessert"]}
            meal_id = self._meals_collection.replace_record(record_id=id, new_record=posted_meal)

        except ResourceNotFound:
            return RESPONSE_CODES["Resource-Does-Not-Exists"]  # -5, 404

        except DishNotFound:
            return RESPONSE_CODES["Dish-ID-Does-Not-Exists"]  # -6, 422

        return meal_id, \
            RESPONSE_CODES["Resource-Modified-Successfully"]  # 200

    def delete(self, id: int = None, name: str = None):
        """
        Handle DELETE /meals/{ID} , /meals/{name} deletes the ID of the dish and removes that dish from /dishes

        Args:
        - dish_id: id of the meal in the collection
        - dish_name:  name of the meal in collection.

        Returns: ID of the deleted meal if exists, else raise an appropriate exception.
        """
        try:
            return self._meals_collection.delete_record(name, id)["ID"], \
                RESPONSE_CODES["Resource-Deleted-Successfully"]  # 200

        except ResourceNotFound:
            return RESPONSE_CODES["Resource-Does-Not-Exists"]  # -5, 404
