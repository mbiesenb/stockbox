from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from authentication.models import BV_Register
from rest_framework import serializers

from django.contrib.auth.models import User


class BV_RegisterSerializer(serializers.ModelSerializer):

    #TODO: Fix the password thing
    username    = serializers.CharField(required=True)
    #password    = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    #password2   = serializers.CharField(write_only=True, required=True)
    password    = serializers.CharField(required=True, validators=[validate_password])
    password2   = serializers.CharField(required=True)
    firstname   = serializers.CharField(required=False)
    lastname    = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    profile_image = serializers.CharField(required=False)

    class Meta:
        model = BV_Register
        fields = ('username', 'password', 'password2', 'firstname', 'lastname', 'description', 'profile_image' )



class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id','username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
    
        user.set_password(validated_data['password'])
        user.save()

        return user