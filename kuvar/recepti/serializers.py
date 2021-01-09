from rest_framework import serializers
from .models import Ingredient, Recipe, Rating
from pyhunter import PyHunter
from django.contrib.auth.models import User


class TopSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='ingredients__name',)
    count = serializers.IntegerField(required=False)
    class Meta:
        model = Ingredient
        fields = ['name','count']

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id','name']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id','user', 'recipe', 'rating']

class RecipeSerializer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField(required=False)
    rating = serializers.SlugRelatedField(many=True, read_only=True, slug_field='rating')
    ing_count = serializers.IntegerField(required=False)
    class Meta:
        model = Recipe
        fields = ['id','created_by', 'name', 'recipe_text', 'ingredients','rating','avg_rating','ing_count']

class UserSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['id','username','first_name', 'last_name', 'email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only':True}}

    def save(self):
        user = User(
                    username = self.validated_data['username'],
                    first_name = self.validated_data['first_name'],
                    last_name = self.validated_data['last_name'],
                    email = self.validated_data['email'],
                    )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializer.ValidationError({'password':'Passwords must match!'})
        user.set_password(password)
        user.save()
        return user

    def validate_email(self, email):
        hunter_key = 'HUNTER_API_KEY'
        hunter = PyHunter(hunter_key)

        if hunter.email_verifier(email)['status'] not in ['valid','webmail']:
            raise serializers.ValidationError('Invalid email address')
        return email
