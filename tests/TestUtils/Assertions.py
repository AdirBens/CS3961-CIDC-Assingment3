import requests


def assert_status_code(response: requests.Response, status_code: int | list[int]):
    if isinstance(status_code, int):
        status_code = [status_code]

    assert response.status_code in status_code


def assert_return_value(response: requests.Response, returned_value: any):
    assert response.json() == returned_value


def assert_unique_resource_id(responses: list[requests.Response]):
    resource_ids = [response.json() for response in responses]
    assert len(set(resource_ids)) == len(resource_ids)


def assert_resource_id_positive_int(response: requests.Response):
    assert response.json() > 0
    assert isinstance(response.json(), int)


def assert_valid_added_resource(response: requests.Response):
    assert_status_code(response, 201)
    assert_resource_id_positive_int(response)


def assert_field_in_range(response: requests.Response, field: str, val_range: tuple[float, float]):
    assert_resource_has_field(response, field)
    field_value = response.json()[field]
    assert val_range[0] <= field_value <= val_range[1]


def assert_resource_has_field(response: requests.Response, field: str):
    assert field in response.json()
