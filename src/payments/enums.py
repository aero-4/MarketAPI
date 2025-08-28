from enum import StrEnum, IntEnum


class PaymentStatus(StrEnum):
    PENDING = "pending"
    EXPIRED = "expired"
    FAIL = "fail"
    SUCCESS = "success"
