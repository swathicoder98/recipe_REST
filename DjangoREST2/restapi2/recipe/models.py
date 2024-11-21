from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    cuisine = models.CharField(max_length=50)
    meal_type = models.CharField(max_length=50)
    ingredients = models.TextField()
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Review(models.Model):
    recipe = models.ForeignKey(Recipe,related_name='reviews',on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    rating = models.IntegerField()      # DecimalField(max_digits=2,decimal_places=1,validator=[MinValueValidator(0.0),MaxValidator(5.0)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.recipe.name} by {self.user.username}"