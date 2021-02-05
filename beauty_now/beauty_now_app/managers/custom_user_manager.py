from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _

from ..models.customer_profile_models import CustomerProfile


class CustomUserManager(BaseUserManager):
    """
    Custom user manager.
    
    Arguments:
        BaseUserManager {class} -- BaseUserManager class.
    """
    
    def create_user(self, email=None, password=None, **extra_fields):
        """
        Create user method.
        
        Keyword Arguments:
            email {string} -- User email address. (default: {None})
            password {string} -- User password. (default: {None})
        
        Returns:
            CustomUser -- Custom user record.
        """
        if email:
            email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.is_active = True

        user.save()

        customer_profile = CustomerProfile(
            custom_user=user,
            customer_profile_id=f'C{user.id * 2 + 100}'
        )

        customer_profile.save()
        
        return user

    
    def create_superuser(self, email, password, **extra_fields):
        """
        Create superuser method.
        
        Arguments:
            email {string} -- User email address.
            password {string} -- User password.
        
        Raises:
            ValueError: Raised if is_staff flag not set to True.
            ValueError: Raised if is_superuser flag not set to True.
        
        Returns:
            CustomUser -- Custom user record.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))

        return self.create_user(email, password, **extra_fields)
