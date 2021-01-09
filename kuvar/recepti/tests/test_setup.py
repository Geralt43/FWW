from rest_framework.test import APITestCase
from django.urls import reverse
from ..models import Ingredient, Recipe
from django.contrib.auth.models import User

class TestSetUp(APITestCase):

    def setUp(self):

        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.users = reverse('users')

        self.user_data = {
            'first_name':'Milos',
            'last_name':'Zzzy',
            'email':'miki@gmail.com',
            'username':'miki99',
            'password':'Cedevita88',
            'password2':'Cedevita88',
        }
        user1 = User.objects.create(first_name='Dragan',last_name='Petrovic',email='dra@gmail.com',username='dragan55',password='koloseum21')
        user2 = User.objects.create(first_name='Petar',last_name='Petrovic',email='pera@gmail.com',username='petar77',password='koloseum21')
        ing1 = Ingredient.objects.create(name='sir')
        ing2 = Ingredient.objects.create(name='jaja')
        r1 = Recipe.objects.create(name='pita',recipe_text='neka pita', created_by=user1)
        r1.ingredients.add(ing1)
        r2 = Recipe.objects.create(name='supa',recipe_text='neka supa', created_by=user2)
        r2.ingredients.add(ing2)

        return super().setUp()
