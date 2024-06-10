import strawberry
from strawberry_django.optimizer import DjangoOptimizerExtension

from main.graphql.subscriptions import Subscription
from .query import Query
from .mutate import Mutation
from gqlauth.core.middlewares import JwtSchema


# schema = JwtSchema(
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
    extensions=[
        DjangoOptimizerExtension,
    ],
)