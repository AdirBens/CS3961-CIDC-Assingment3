from TestUtils import RestApiAgent, Assertions


def test_create_new_dishes():
    """
    [TEST 1]
    Execute three POST /dishes requests using the dishes, “orange”, “spaghetti”, and “apple pie”.
    The test is successful if:
        1. All 3 requests return unique IDs (none of the IDs are the same).
        2. The return status code from each POST request is 201.
    """
    DISHES_TO_CREATE = ["orange", "spaghetti", "apple pie"]
    responses = []

    for dish in DISHES_TO_CREATE:
        response = RestApiAgent.add_dish(dish)
        Assertions.assert_valid_added_resource(response)
        responses.append(response)

    Assertions.assert_unique_resource_id(responses)


def test_orange_dish_sanity():
    """
    [TEST 2]
    Execute a GET dishes/<orange-ID> using the ID of the orange dish.
    The test is successful if:
        1. The sodium field of the return JSON object is between .9 and 1.1.
        2. The return status code from the request is 200.
    """
    ORANGE_ID = 1
    orange_resource = RestApiAgent.get_dish_by_id(ORANGE_ID)

    Assertions.assert_status_code(response=orange_resource, status_code=200)
    Assertions.assert_field_in_range(response=orange_resource, field="sodium", val_range=(0.9, 1.1))


def test_get_all_dishes_sanity():
    """
    [TEST 3]
    Execute a GET /dishes request.
    The test is successful if:
        1. The returned JSON object has 3 embedded JSON objects (dishes)
        2. The return status code from the GET request is 200.
    """
    EXPECTED_NUM_DISHES = 3
    all_dishes = RestApiAgent.get_dishes()

    assert len(all_dishes.json()) == EXPECTED_NUM_DISHES
    Assertions.assert_status_code(response=all_dishes, status_code=200)


def test_add_non_exists_dish():
    """
    [TEST 4]
    Execute a POST /dishes request supplying the dish name “blah”.
    The test is successful if:
        1. The return value is -3
        2. The return code is 404 or 400 or 422.
    """
    NON_EXIST_DISH_NAME = "blah"
    POSSIBLE_SATUS_CODES = [400, 404, 422]
    EXPECTED_RETURN_VALUE = -3
    non_exists_response = RestApiAgent.add_dish(NON_EXIST_DISH_NAME)

    Assertions.assert_return_value(response=non_exists_response, returned_value=EXPECTED_RETURN_VALUE)
    Assertions.assert_status_code(response=non_exists_response, status_code=POSSIBLE_SATUS_CODES)


def test_add_already_exists_dish():
    """
    [TEST 5]
    Perform a POST dishes request with the dish name “orange”.
    The test is successful if:
        1. The return value is -2 (same dish name as existing dish)
        2. The return status code is 400 or 404 or 422.
    """
    DISH_NAME = "orange"
    POSSIBLE_SATUS_CODES = [400, 404, 422]
    EXPECTED_RETURN_VALUE = -2
    response = RestApiAgent.add_dish(DISH_NAME)

    Assertions.assert_return_value(response=response, returned_value=EXPECTED_RETURN_VALUE)
    Assertions.assert_status_code(response=response, status_code=POSSIBLE_SATUS_CODES)


def test_create_meal():
    """
    [TEST 6]
    Perform a POST /meals request specifying that the meal name is “delicious” s.t.
        { name: "delicious", appetizer: 1 (orange id), main: 2 (spaghetti id), dessert: 3 (apple pie id) }
    The test is successful if:
        1. The returned value ID > 0
        2. The return status code is 201.
    """
    MEAL_NAME = "delicious"
    create_meal_response = RestApiAgent.add_meal(name=MEAL_NAME, appetizer_id=1, main_id=2, dessert_id=3)

    Assertions.assert_resource_id_positive_int(create_meal_response)
    Assertions.assert_valid_added_resource(create_meal_response)


def test_get_all_meals_sanity():
    """
    [TEST 7]
    Perform a GET /meals request.
    The test is successful if:
        1. The returned JSON object has 1 meal.
        2. The return status code is 200.
    """
    EXPECTED_NUM_MEALS = 1
    all_meals = RestApiAgent.get_meals()

    assert len(all_meals.json()) == EXPECTED_NUM_MEALS
    Assertions.assert_status_code(response=all_meals, status_code=200)


def test_add_already_exists_meal():
    """
    [TEST 8]
    Perform a POST /meals request as in test 6 with the same meal name (and courses can be the same or different)
    The test is successful if:
        1. The returned value code is -2 (same meal name as existing meal)
        2. The return status code is 400 or 422.
    """
    MEAL_NAME = "delicious"
    POSSIBLE_SATUS_CODES = [400, 422]
    EXPECTED_RETURN_VALUE = -2
    already_exists_meal_response = RestApiAgent.add_meal(name=MEAL_NAME, appetizer_id=1, main_id=2, dessert_id=3)

    Assertions.assert_status_code(response=already_exists_meal_response, status_code=POSSIBLE_SATUS_CODES)
    Assertions.assert_return_value(response=already_exists_meal_response, returned_value=EXPECTED_RETURN_VALUE)
