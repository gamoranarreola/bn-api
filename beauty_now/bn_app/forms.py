from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from beauty_now.bn_app.models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser

        fields = (
            'email',
            'last_name',
            'first_name',
        )


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser

        fields = (
            'email',
            'last_name',
            'first_name'
        )
