from django.urls import path
from recepti import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('recipe/', views.recipe_list),
    path('recipe/<int:pk>/', views.recipe_detail),
    path('ingredients/', views.ingredient_list),
    path('registration/', views.user_registration, name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token_refresh/', TokenRefreshView.as_view()),
    path('users/', views.UserList.as_view(), name='users'),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('myrecipes/', views.my_recipes),
    path('rate_recipe/', views.rate_recipe),
    path('top_ingredients/', views.get_top_ing),
    path('search_recipe/', views.SearchRecipe.as_view()),
    path('ingredients_filter/', views.IngredientFilter.as_view()),

]
