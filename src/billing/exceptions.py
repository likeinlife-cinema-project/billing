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


class NotFoundPaymentException(BaseError):
    detail = "Not found payment to refund"
    status_code = HTTPStatus.BAD_REQUEST


class WrongUserSubscriptionException(BaseError):
    detail = "Wrong user subscription id"
    status_code = HTTPStatus.BAD_REQUEST


class ExpiredSubscriptionException(BaseError):
    detail = "User subscription is already expired"
    status_code = HTTPStatus.BAD_REQUEST
