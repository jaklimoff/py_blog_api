from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

__author__ = 'jaklimoff'


class EmailAuthBackend(ModelBackend):
    def authenticate(self, email=None, password=None, **kwargs):
        if email is None:
            email = kwargs.get('username')

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                user.backend = "%s.%s" % (self.__module__, self.__class__.__name__)
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None