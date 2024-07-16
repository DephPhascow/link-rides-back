from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserModel

class UserModelCreationForm(UserCreationForm):

    class Meta:
        model = UserModel
        fields = ("tg_id",)


class UserModelChangeForm(UserChangeForm):

    class Meta:
        model = UserModel
        fields = ("tg_id",)
