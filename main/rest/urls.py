from django.urls import path
from .views import (
    TmpApiView,
)

urlpatterns = [
    path('tmp/', TmpApiView.as_view()),
]