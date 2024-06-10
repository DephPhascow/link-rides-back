import strawberry_django
from strawberry import auto
from main import models
from main.graphql import filters, orders

@strawberry_django.type(models.TmpModel, filters=filters.TmpFilter, order=orders.TmpOrder, pagination=True, )
class TmpType:
    name: auto
    description: str