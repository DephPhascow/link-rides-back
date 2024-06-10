import strawberry
from main import models

@strawberry.django.order(models.TmpModel)
class TmpOrder:
    name: strawberry.auto
    description: str
