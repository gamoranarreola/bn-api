from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import AuthUser


class AuthUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = AuthUser

        fields = (
            'email',
            'last_name',
            'first_name',
        )


class AuthUserChangeForm(UserChangeForm):

    class Meta:
        model = AuthUser

        fields = (
            'email',
            'last_name',
            'first_name'
        )
