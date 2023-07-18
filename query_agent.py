import json

import requests

QUERIES_FILE_PATH = r"./query.txt"
API_DISH_ADDRESS = "http://127.0.0.1:8000/dishes"


def run_queries():
    with open(QUERIES_FILE_PATH, "r") as query_file:
        queries = query_file.readlines()

    for query in queries:
        dish_id = _post_dish(dish_name=query.strip())

        if dish_id > 0:
            dish_data = _get_dish_data(dish_id=dish_id)
            print("{name} contains {cal} calories, {sodium} mgs of sodium, and {sugar} grams of sugar".format(**dish_data))
        else:
            print("No Data found for dish with name: {name}.".format(name=query.strip()))



def _post_dish(dish_name: str) -> int:
    response = requests.post(url=API_DISH_ADDRESS,
                             headers={"Content-Type": "application/json"},
                             data=json.dumps({"name": dish_name}))

    return response.json()


def _get_dish_data(dish_id: int) -> dict:
    response = requests.get(url=f"{API_DISH_ADDRESS}/{dish_id}",
                            headers={"Content-Type": "application/json"})

    return response.json()


def main():
    run_queries()


if __name__ == "__main__":
    main()
