import typing
from strawberry.types import Info
from strawberry.permission import BasePermission

class IsAuthenticated(BasePermission):
    message = "Нет доступа"
    def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        user = info.context["request"].user
        return user and user.is_authenticated
