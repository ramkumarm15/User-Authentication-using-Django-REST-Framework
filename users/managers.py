from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    '''
    Custom user manager to create user and superuser
    '''
    use_in_migrations = True

    def _create_user(self, username, email, name, password, **kwargs):
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, name=name, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, name, password=None, **kwargs):
        kwargs.setdefault('is_superuser', False)
        kwargs.setdefault('is_staff', False)
        return self._create_user(username, email, name, password, **kwargs)

    def create_superuser(self, username, email, name, password, **kwargs):

        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_superuser') is not True:
            return ValueError('Superuser must have is_superuser = True')

        if kwargs.get('is_staff') is not True:
            return ValueError('Superuser must have is_staff = True')

        return self._create_user(username, email, name, password, **kwargs)
