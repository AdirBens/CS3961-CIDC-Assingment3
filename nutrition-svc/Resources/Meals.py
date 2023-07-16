from flask import request
from flask_restful import Resource, reqparse

from Common.Collections.DishesCollection import DishesCollection
from Common.Collections.MealsCollection import MealsCollection
from Utils.Helpers import arg_parser
from Common.Exceptions import InvalidBodyParameter, MissingBodyParameter, DishNotFound, ResourceAlreadyExists
from Common.StatusCodes import RESPONSE_CODES


class Meals(Resource):
    _POST_BODY_PARAMS = {'name': str, 'appetizer': int,
                         'main': int, 'dessert': int}
    _meals_collection = MealsCollection()
    _dishes_collection = DishesCollection()

    def get(self):
        """
        :return: all meals indexed by ID
        """
        return self._meals_collection.fetch_all(), RESPONSE_CODES["Resource-Get-Successfully"]  # 200

    def post(self):
        """
        Handle POST /meals request: Add new dish to dishes collection.

        Args:
        - in message body = json contains meal name, appetizer, main, dessert.

        Returns:
        - if successfully, returns meal ID (positive integer) and code 201 (resource successfully created)
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
            args = arg_parser(parser, self._POST_BODY_PARAMS)

        except MissingBodyParameter or InvalidBodyParameter:
            return RESPONSE_CODES["Invalid-Body-Parameters"]  # -1, 422

        try:
            meal_record = {"name": args["name"],
                           "appetizer": args["appetizer"],
                           "main": args["main"],
                           "dessert": args["dessert"]}
            meal_id = self._meals_collection.insert_record(record=meal_record)

        except DishNotFound:
            return RESPONSE_CODES["Dish-ID-Does-Not-Exists"]  # -6, 422

        except ResourceAlreadyExists:
            return RESPONSE_CODES["Resource-Already-Exists"]  # -2, 422

        return meal_id, \
            RESPONSE_CODES["Resource-Created-Successfully"]  # 201
