from flask import request
from flask_restful import Resource, reqparse

from Common.Collections.DishesCollection import DishesCollection
from Common.Exceptions import ResourceAlreadyExists, ApiNinjaUnreachable, ApiNinjaCantFindName, MissingBodyParameter, \
    InvalidBodyParameter
from Common.StatusCodes import RESPONSE_CODES
from Utils.ApiNinjaAgent import ApiNinjaAgent
from Utils.Helpers import arg_parser


class Dishes(Resource):
    """
    Dishes resource holds store a collection of dishes and theirs nutrition information.
    A dish is given by its name, for example:
        - 'peanut butter and jelly sandwich'
        - 'chicken soup'
        etc..
    """
    _POST_BODY_PARAMS = {'name': str}
    _dishes_collection = DishesCollection()
    _ninja_agent = ApiNinjaAgent()

    def get(self):
        """
        Returns all dishes
        """
        return self._dishes_collection.fetch_all(), RESPONSE_CODES["Resource-Get-Successfully"]  # 200

    def post(self):
        """
        Handle POST /dishes requests, Add new dish to dishes collection.

        Args:
        - in message body = name: 'dish name'

        Returns:
        - if successfully, returns dish ID (positive integer) and code 201 (resource successfully created)
                     api ninjas - make sure that handling if it returns multiple components in an array
        - could also return non-positive ID with:
            * 0 if request content-type is not application/json (status code 415)
            * -1 if 'name' parameter was not specified in message body (status code 422)
            * -2 if dish og a given name already exists (status code 422)
            * -3 is api-ninjas API does not recognize this dish name (status code 422)
            * -4 if api-ninja API not reachable (status code 504)
        """
        if request.headers.get('Content-Type', '') != 'application/json':
            return RESPONSE_CODES["Content-Type-Exception"]  # 0, 415

        parser = reqparse.RequestParser()
        try:
            args = arg_parser(parser, self._POST_BODY_PARAMS)

        except MissingBodyParameter or InvalidBodyParameter:
            return RESPONSE_CODES["Invalid-Body-Parameters"]

        dish_name = args['name']
        try:
            dish_record = self._ninja_agent.query(query_string=dish_name)
            dish_record["name"] = dish_name
            dish_id = self._dishes_collection.insert_record(dish_record)

        except ResourceAlreadyExists:
            return RESPONSE_CODES["Resource-Already-Exists"]  # -2, 422

        except ApiNinjaCantFindName:
            return RESPONSE_CODES["Void-Query-Results"]  # -3, 422

        except ApiNinjaUnreachable:
            return RESPONSE_CODES["Out-Source-Unreachable"]  # -4, 504

        return dish_id, \
            RESPONSE_CODES["Resource-Created-Successfully"]  # 201

    def delete(self):
        """
        Delete Dishes is not allowed.
        """
        return RESPONSE_CODES["Invalid-Method"]  # "This method is not allowed for the requested URL", 405
