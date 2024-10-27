import requests
from enum import Enum


class Methods(Enum):
    GET = "GET"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    POST = "POST"


class APIObject:

    def __init__(self, url: str, method: Methods, headers: dict = None, params: dict = None, body: dict = None):
        self.url = url
        self.method = method
        self.headers = headers
        self.params = params
        self.body = body

    def call(self, retries=1):
        for _ in range(retries):
            try:
                return call_api(self.url, self.method, self.headers, self.params, self.body)
            except Exception as e:
                print(f"Failed to call {self.url}")
                print(e)

        raise RuntimeError("Failed to call api")

    def check_call(self, status_code: int, response_value, retries=1):
        response_object = self.call(retries=retries)
        assert status_code == response_object.status_code
        if isinstance(response_value, dict):
            for key, value in response_value.items():
                assert key in response_object.json()
                assert value == response_object.json()[key]
            return response_object.json()
        elif isinstance(response_value, str):
            assert response_value == response_object.text
            return response_object.text


def call_api(url: str, method: Methods, headers: dict, params: dict = None, body: dict = None):
    if not url:
        raise ValueError("url not specified")

    # TODO: add more validations
    return requests.request(method=method.value, url=url, headers=headers, params=params, json=body)


def create_booking_object(firstname, lastname, totalprice, depositpaid, checkin, checkout, additionalneeds):
    return {
        "firstname": firstname,
        "lastname": lastname,
        "totalprice": totalprice,
        "depositpaid": depositpaid,
        "bookingdates": {
            "checkin": checkin,
            "checkout": checkout
        },
        "additionalneeds": additionalneeds
     }
