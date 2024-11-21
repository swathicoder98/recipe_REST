from django.urls import path,include
from rest_framework.routers import DefaultRouter
from recipe import views
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegisterView

router = DefaultRouter()
router.register(r'recipes',views.RecipeViewSet)
router.register(r'reviews',views.ReviewViewSet)
router.register(r'users',views.UserViewSet)

urlpatterns = [
    path("",include(router.urls)),
    path('register/',views.RegisterView.as_view(),name='register'),
    path('search_ingredient/', views.Search_ingredient.as_view(), name='search_ingredient'),
    path('search_cuisine/', views.Search_cuisine.as_view(), name='search_cuisine'),
    path('search_meal/', views.Search_meal.as_view(), name='Search_meal'),
    path('search_name/', views.Search_name.as_view(), name='search_name'),

    path('login/',obtain_auth_token,name='login'),

]
