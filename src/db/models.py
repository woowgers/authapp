from dataclasses import dataclass
from enum import Enum


class UserType(Enum):
    ADMIN = "admin"
    CASHIER = "cashier"
    CUSTOMER = "customer"


@dataclass
class User:
    user_id: int
    email: str
    type: UserType
    name: str
    pw_hash: bytes

    @property
    def is_admin(self):
        return self.type == UserType.ADMIN.value

    @property
    def is_cashier(self):
        return self.type == UserType.CASHIER.value

    @property
    def is_customer(self):
        return self.type == UserType.CUSTOMER.value

