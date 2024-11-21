from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import Recipe,Review
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id','username','password','email','first_name','last_name']

    def create(self,validated_data):  #after validation validated_data ie deserialized data sent to create()  fn
        user=User.objects.create_user(username=validated_data['username'],
                                      password=validated_data['password'],
                                      email=validated_data['email'],
                                      first_name=validated_data['first_name'],
                                      last_name=validated_data['last_name'])
        return user


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ['id','name','description','cuisine','meal_type','ingredients','instructions','created_by','created_at']
class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id', 'recipe', 'user', 'rating', 'comment','created_at']




class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

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