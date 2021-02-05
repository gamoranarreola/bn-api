from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from ..models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Custom user creation form.
    
    Arguments:
        UserCreationForm {class} -- UserCreationForm class.
    """
    class Meta(UserCreationForm):
        model = CustomUser

        fields = (
            'email',
            'last_name',
            'first_name',
        )


class CustomUserChangeForm(UserChangeForm):
    """
    Custom user change form.
    
    Arguments:
        UserChangeForm {class} -- UserChangeForm class.
    """
    class Meta:
        model = CustomUser

        fields = (
            'email',
            'last_name',
            'first_name'
        )
