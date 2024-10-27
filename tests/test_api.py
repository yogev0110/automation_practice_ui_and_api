from utils.api import APIObject, Methods, create_booking_object
from utils.common import check_test, get_dates


BOOKING_URL = "https://restful-booker.herokuapp.com/booking"


class APITestObject:
    def __init__(self, api_object: APIObject, expected_status_code, expected_response_object):
        self.api_object = api_object
        self.expected_status_code = expected_status_code
        self.expected_response_object = expected_response_object

    def test(self):
        return self.api_object.check_call(self.expected_status_code, self.expected_response_object)


@check_test
def test_question_one():
    start_date, end_date = get_dates(offset=7, delta=2)
    example_booking = create_booking_object(
        firstname="Yogev",
        lastname="Cohen",
        totalprice=200,
        depositpaid=True,
        checkin=start_date,
        checkout=end_date,
        additionalneeds="none"
    )
    headers = {"Content-Type": "application/json"}

    api_object = APIObject(url=BOOKING_URL, method=Methods.POST, headers=headers, body=example_booking)
    expected_booking_resource = {
        "booking": example_booking,
    }

    response = APITestObject(api_object, 200, expected_booking_resource).test()
    assert "bookingid" in response
    booking_id = response["bookingid"]
    assert isinstance(booking_id, int)

    get_object = APIObject(url=f"{BOOKING_URL}", method=Methods.GET)
    booking_list_api_object = get_object.call().json()
    assert any([booking['bookingid'] == booking_id for booking in booking_list_api_object])

    api_object = APIObject(url=f"{BOOKING_URL}/{booking_id}", method=Methods.GET)
    APITestObject(api_object, 200, example_booking).test()


@check_test
def test_question_two():
    start_date, end_date = get_dates(offset=7, delta=4)
    example_booking = create_booking_object(
        firstname="Yogev",
        lastname="Cohen",
        totalprice=300,
        depositpaid=True,
        checkin=start_date,
        checkout=end_date,
        additionalneeds="none"
    )
    headers = {"Content-Type": "application/json"}

    api_object = APIObject(url=BOOKING_URL, method=Methods.POST, headers=headers, body=example_booking)
    expected_booking_resource = {
        "booking": example_booking,
    }

    response = APITestObject(api_object, 200, expected_booking_resource).test()
    assert "bookingid" in response
    booking_id = response["bookingid"]
    assert isinstance(booking_id, int)

    get_object = APIObject(url=f"{BOOKING_URL}", method=Methods.GET)
    booking_list_api_object = get_object.call().json()
    assert any([booking['bookingid'] == booking_id for booking in booking_list_api_object])

    api_object = APIObject(url=f"{BOOKING_URL}/{booking_id}", method=Methods.GET)
    APITestObject(api_object, 200, example_booking).test()

    _, end_date = get_dates(offset=7, delta=5)
    example_booking["bookingdates"]["checkout"] = end_date
    headers["Cookie"] = 'token=abc123'
    headers["Authorization"] = 'Basic YWRtaW46cGFzc3dvcmQxMjM='
    api_object = APIObject(url=f"{BOOKING_URL}/{booking_id}", method=Methods.PUT, headers=headers, body=example_booking)
    APITestObject(api_object, 200, example_booking).test()
