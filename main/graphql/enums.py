from strawberry import enum
from enum import Enum

@enum
class UserDriveType(Enum):
    PASSENGER = "passenger"
    TAXI = "taxi"