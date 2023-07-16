import requests
import json

from Common import Config
from Common.Exceptions import ApiNinjaUnreachable, ApiNinjaCantFindName

from Utils.Helpers import flatten_json


class ApiNinjaAgent(object):
    """
    Agent for 'Api-Ninjas' services.
    """
    def __init__(self, configuration=Config.Common):
        self._api_url = configuration.NinjaApi_BaseURL
        self._api_key = configuration.NinjaApi_Key

    def __str__(self) -> str:
        return f"Api-Ninjas Adapter \n [+] Base URL: {self._api_url}\n [+] X-Api-Key: {self._api_url}"

    def query(self, query_string: str) -> json:
        """
        Fetch data from Api-Ninjas services using this agent.
        In case of multiple responses, the agent merges the responses fields one-by-one to get
        unified json contains all data.

        Args:
        - query_string - the query to run on Api-Ninjas services.

        Returns: json contains the retrieved dish data.
        """
        try:
            response = requests.request(method="GET",
                                        url=self._api_url,
                                        headers={'X-Api-Key': self._api_key},
                                        params={'query': query_string.strip()})

        except ConnectionError:
            raise ApiNinjaUnreachable()

        if len(response.json()) == 0:
            raise ApiNinjaCantFindName()

        return self._data_to_dish_record(response.json())

    @staticmethod
    def _data_to_dish_record(response_data: json):
        names_resolver = {'calories': 'cal', 'serving_size_g': 'size', 'sodium_mg': 'sodium',
                          'sugar_g': 'sugar', 'name': 'name'}
        dish_record_keys = ['name', 'cal', 'size', 'sodium', 'sugar']

        dish_record = flatten_json(response_data)
        dish_record = {names_resolver.get(key, key): dish_record[key] for key in dish_record.keys()}
        dish_record = {key: dish_record[key] for key in dish_record.keys() if key in dish_record_keys}

        return dish_record
