from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from .models import Ingredient, Recipe, Rating
from .serializers import RecipeSerializer, IngredientSerializer, RatingSerializer, UserSerializer, TopSerializer
from django.db.models import Avg, Count
from rest_framework import filters

# Create your views here.
class UserList(generics.ListAPIView):
    """
    Return all Users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    """
    Return a specific user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET'])
def get_top_ing(request):
    """
    Gets back top 5 used ingredients
    """
    ingredients = Recipe.objects.values('ingredients__name').annotate(count=Count('ingredients__id')).order_by('-count')[:5]
    #print(ingredients)
    serializer = TopSerializer(ingredients,many=True)
    return Response(serializer.data)


@api_view(['POST','PUT'])
def rate_recipe(request):
    """
    Rate Recipe or Update existing rating
    """
    try:
        recipe = Recipe.objects.get(id=request.data['recipe'])
    except (ObjectDoesNotExist, ValueError) as e:
        #print(e)
        return Response({"recipe":["This field is requered"]})
    if request.method == 'POST':
        try:
            rating = Rating.objects.get(user_id=request.user.id,recipe_id=request.data['recipe'])
        except ObjectDoesNotExist as e:
            rating = None
        else:
            return Response('Rating already exists, you can only update it!', status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if recipe.created_by == request.user:
            print(recipe.created_by,request.user)
            return Response("Can't rate your own Recipes!", status=status.HTTP_403_FORBIDDEN)
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        recipe = Recipe.objects.get(id=request.data['recipe'])
        try:
            rating = Rating.objects.get(user_id=request.user.id,recipe_id=request.data['recipe'])
        except (ObjectDoesNotExist, ValueError) as e:
            return Response("You have not rated this Recipe, can't update!", status=status.HTTP_403_FORBIDDEN)
        if recipe.created_by == request.user:
            #print(recipe.created_by,request.user)
            return Response("Can't rate your own Recipes!", status=status.HTTP_403_FORBIDDEN)
        serializer = RatingSerializer(rating,data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=request.user.id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def my_recipes(request):
    """
    Get Recipes for Currently Authenticated Used
    """
    #recipes = Recipe.objects.filter(created_by=request.user)
    recipes = Recipe.objects.filter(created_by=request.user).annotate(avg_rating=Avg('rating__rating'))
    serializer = RecipeSerializer(recipes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_registration(request):
    """
    Create a new User
    """
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'New User Created'
            data['email'] = user.email
            data['username'] = user.username
            data['first_name'] = user.first_name
            data['last_name'] = user.last_name
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_201_CREATED)


@api_view(['GET','POST'])
def recipe_list(request):
    """
    List all Recipes or create a new Recipe
    """
    if request.method == 'GET':
        recipes = Recipe.objects.all().annotate(avg_rating=Avg('rating__rating'))
        #recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        print(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT'])
def recipe_detail(request,pk):
    """
    Retrive, update, or delete a recipe
    """
    try:
        recipe = Recipe.objects.get(pk=pk)
    except Recipe.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = RecipeSerializer(recipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def ingredient_list(request):
    """
    List all Ingredients
    """
    if request.method == 'GET':
        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SearchRecipe(generics.ListAPIView):
    """
    Search for a Recipe by Name, Text, Ingredients
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'recipe_text','ingredients__name']

class IngredientFilter(generics.ListAPIView):
    serializer_class = RecipeSerializer
    def get_queryset(self):
        """
        Filter Recipes by min and max number of Ingredients
        """
        qs = Recipe.objects.annotate(ing_count=Count('ingredients'))
        #print(qs)
        min = self.request.query_params.get('min', default='0')
        max = self.request.query_params.get('max', default='30')
        qs = qs.filter(ing_count__gte=min, ing_count__lte=max)
        return qs
