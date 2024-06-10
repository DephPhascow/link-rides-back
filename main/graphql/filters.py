import strawberry
from strawberry import auto
from main import models
import typing

@strawberry.django.filter(models.TmpModel, lookups=True)
class TmpFilter:
    id: auto
    name: auto
    description: typing.Optional[str]
