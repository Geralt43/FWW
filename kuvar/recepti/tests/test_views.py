from .test_setup import TestSetUp
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from recepti import views

class TestViews(TestSetUp):

    def test_registration_no_data(self):
        response = self.client.post(self.register_url)
        self.assertEqual(response.status_code, 400)

    def test_registration_good_data(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_user_not_authenticated(self):
        response = self.client.post(self.login_url, self.user_data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_registered_user_can_authenticate(self):
        response1 = self.client.post(self.register_url, self.user_data, format='json')
        response2 = self.client.post(self.login_url, self.user_data, format='json')
        self.assertEqual(response2.status_code, 200)

    def test_user_can_see_all_users(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='dragan55')
        view = views.UserList.as_view()
        request = factory.get(self.users)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_user_can_see_all_recipes(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='dragan55')
        view = views.recipe_list
        request = factory.get(self.users)
        force_authenticate(request,user=user)
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_user_can_see_all_ingredients(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='dragan55')
        view = views.ingredient_list
        request = factory.get(self.users)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_user_can_see_his_recipes(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='dragan55')
        view = views.my_recipes
        request = factory.get(self.users)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_user_can_see_top_ingredients(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='dragan55')
        view = views.get_top_ing
        request = factory.get(self.users)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_user_can_create_recipe(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='dragan55')
        view = views.recipe_list
        request = factory.post(view, {'name':'Torta', 'recipe_text':'neka torta','ingredients':1})
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, 201)

    def test_user_search_for_recipe(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='dragan55')
        view = views.SearchRecipe.as_view()
        request = factory.get(view, {'search':'supa'})
        force_authenticate(request, user=user)
        response = view(request)
        #import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, 200)

    def test_user_can_rate_recipe(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='dragan55')
        view = views.rate_recipe
        request = factory.post(view, {'recipe':'2','rating':'2.0'})
        force_authenticate(request, user=user)
        response = view(request)
        #import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, 201)

    def test_user_cannot_rate_his_own_recipe(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='dragan55')
        view = views.rate_recipe
        request = factory.post(view, {'recipe':'1','rating':'2.0'})
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, 403)

    def test_user_cannot_rate_already_rated_recipe(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='dragan55')
        view = views.rate_recipe
        request1 = factory.post(view, {'recipe':'2','rating':'2.0'})
        force_authenticate(request1, user=user)
        response = view(request1)
        request2 = factory.post(view, {'recipe':'2','rating':'4.0'})
        force_authenticate(request2, user=user)
        response = view(request2)
        self.assertEqual(response.status_code, 405)

    def test_user_cannot_update_rating_on_his_own_recipe(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='dragan55')
        view = views.rate_recipe
        request = factory.put(view, {'recipe':'1','rating':'2.0'})
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, 403)
