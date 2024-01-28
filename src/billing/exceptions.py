from rest_framework.exceptions import APIException


class WrongEventException(APIException):
    status_code = 400
    default_detail = "Wrong event type received from payment service"
    default_code = "Bad request"
