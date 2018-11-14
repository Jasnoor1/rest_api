from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from rest_framework import exceptions
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    print('I am in serializer class')
    email = serializers.EmailField(required=True,
                                   validators=[UniqueValidator(queryset=User.objects.all())]
                                   )
    username = serializers.CharField(
                                    validators=[UniqueValidator(queryset=User.objects.all())]
                                     )
    password = serializers.CharField(min_length=8)

    print(email,username,password)
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],
                                        validated_data['email'],
                                        validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')



# for login serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username', '')
        password = data.get('password', '')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    msg ='User is deactivated.'
                    raise exceptions.ValidationError(msg)
            else:
                msg='Unable to login with given credentials.'
                raise exceptions.ValidationError(msg)

        else:
            msg = 'Must provide username and password both.'
            raise exceptions.ValidationError(msg)
        return data