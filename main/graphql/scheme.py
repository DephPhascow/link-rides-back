from strawberry_django.optimizer import DjangoOptimizerExtension
from strawberry import relay, ID
# from main.graphql.subscriptions import Subscription
from .query import Query
from .mutate import Mutation
from gqlauth.core.middlewares import JwtSchema
from strawberry.schema.types.scalar import DEFAULT_SCALAR_REGISTRY

schema = JwtSchema(
    query=Query,
    mutation=Mutation,
    # subscription=Subscription,
    extensions=[
        DjangoOptimizerExtension,
    ],
    scalar_overrides={relay.GlobalID: DEFAULT_SCALAR_REGISTRY[ID]},
)