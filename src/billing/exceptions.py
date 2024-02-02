from http import HTTPStatus

from config.base_error import BaseError


class WrongEventException(BaseError):
    detail = "Wrong type in webhook event"
    status_code = HTTPStatus.BAD_REQUEST


class UntrustedIpException(BaseError):
    detail = "Untrusted IP"
    status_code = HTTPStatus.FORBIDDEN


class PaymentGatewayException(BaseError):
    detail = "Error in payment gateway request"
    status_code = HTTPStatus.BAD_REQUEST


class PaymentFailureException(BaseError):
    detail = "Got unknown error in payments processing"
    status_code = HTTPStatus.BAD_REQUEST


class IdempotencyException(BaseError):
    detail = "Idempotency violation"
    status_code = HTTPStatus.FORBIDDEN


class UserTokenException(BaseError):
    detail = "Token invalid"
    status_code = HTTPStatus.UNAUTHORIZED
