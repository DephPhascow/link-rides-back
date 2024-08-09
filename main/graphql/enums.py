from strawberry import enum
from enum import Enum

@enum
class UserDriveType(Enum):
    PASSENGER = "passenger"
    TAXI = "taxi"
    
@enum
class DrivingStatus(Enum):
    WAIT = 'WAIT'
    DRIVE = 'DRIVE'
    REST = 'REST'
    
@enum
class TopByEnum(Enum):
    TAXI = 'TAXI'
    PASSENGER = 'PASSENGER'
    ALL = 'ALL'