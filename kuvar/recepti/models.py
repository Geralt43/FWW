from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Ingredient(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Recipe(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50)
    recipe_text = models.TextField()
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        return self.name

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='rating')
    number_rating=[('5.0','5.0'),('4.0','4.0'),('3.0','3.0'),('2.0','2.0'),('1.0','1.0')]
    rating = models.CharField(max_length=20, choices=number_rating)

    def __str__(self):
        return self.number
