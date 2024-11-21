from django.shortcuts import render
from rest_framework import viewsets,permissions,status,filters
from .models import Recipe,Review
from .serializers import ReviewSerializer,RecipeSerializer,UserSerializer,RegisterSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['cuisine', 'meal_type', 'ingredients','name']

    def perform_create(self,serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False,methods=['get'])
    def search(self,request):
        query = request.query_params.get('q',None)    # use key : q and value : burger ,in params in postman
        if query:
            recipes = Recipe.objects.filter(Q(name__icontains=query) | Q(ingredients__icontains=query))
            serializer = self.get_serializer(recipes,many=True)
            return Response(serializer.data)
        return Response([])

class Search(APIView):
    def get(self,request):
        query = request.query_params.get('search')
        if query:
            r=Recipe.objects.filter(Q(cuisine__icontains=query) | Q(meal_type__icontains=query) | Q(ingredients__icontains=query))
            rs=RecipeSerializer(r,many=True)
            return Response(rs.data,status=status.HTTP_200_OK)

class Search_name(APIView):
    def get(self,request):
        query = request.query_params.get('name')
        if query:
            r=Recipe.objects.filter(name=query)
            rs=RecipeSerializer(r,many=True)
            return Response(rs.data,status=status.HTTP_200_OK)

class Search_meal(APIView):

    def get(self,request):
        query = request.query_params.get('meal')
        if query:
            r=Recipe.objects.filter(meal_type=query)
            rs=RecipeSerializer(r,many=True)
            return Response(rs.data,status=status.HTTP_200_OK)

class Search_ingredient(APIView):
    def get(self, request):
        query = request.query_params.get('ingredients', None)
        if query:
            recipes = Recipe.objects.filter(ingredients__icontains=query)  # Case-insensitive search
            rs = RecipeSerializer(recipes, many=True)
            return Response(rs.data, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_200_OK)  # Return empty list if no query provided

class Search_cuisine(APIView):

    def get(self,request):
        query = request.query_params.get('cuisine')
        if query:
            r=Recipe.objects.filter(cuisine=query)
            rs=RecipeSerializer(r,many=True)
            return Response(rs.data,status=status.HTTP_200_OK)
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self,request):
       serializer_class = UserSerializer(data=request.data)
       if serializer_class.is_valid():
             user = serializer_class.save()
            # Generate token for the new user
             token,created = Token.objects.get_or_create(user=user)
             return Response({ "message":"User registered successfully" ,"token":token.key},status=status.HTTP_201_CREATED)
       return Response(serializer_class.errors,status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    permission_classes=[IsAuthenticated]     #IF LOGGED IN
    def get(self,request):
        self.request.user.auth_token.delete()    #TOKEN OF USER DELETED FROM TABLE
        return Response({'msg':"logout successfully"},status=status.HTTP_200_OK)