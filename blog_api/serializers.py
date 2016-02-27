from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from rest_framework import exceptions
from blog_api.models import Post


__author__ = 'jaklimoff'

from rest_framework import serializers


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('email')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg)
        attrs['user'] = user
        return attrs

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('id', )

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data.get('email'),
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        user.set_password(validated_data.get('password'))
        user.save()
        return user


class PostSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('__all__')

    def is_valid(self, raise_exception=False):
        return super(PostSerializer, self).is_valid(raise_exception)



