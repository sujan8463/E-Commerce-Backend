from django.shortcuts import render
from django.contrib.auth.models import Group, User
from rest_framework import permissions,viewsets
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from .models import Category,Product,CartItem,Order,OrderItem,Payment
from .serializers import UserSerializer,GroupSerializer,CategorySerializer,ProductSerializer,CartItemSerializer,orderSerializer,OrderItemSerializer,PaymentSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import DjangoModelPermissions,IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import filters



class DashboardView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    permission_classes = []
    
class RegisterView(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    
    def create(self,request):
        password = request.data.get("password")
        hash_password = make_password(password)
        data = request.data.copy()
        data['password'] = hash_password
        serializer = UserSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)       

    
class LoginView(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    permission_classes = []
    
    def create(self,request):
        username = request.data.get("username")
        password = request.data.get("password")
        
        user = authenticate(username = username, password=password)
        
        if user == None:
            return Response({'detail':"invalid creditnails"},status=status.HTTP_401_UNAUTHORIZED)
        else:
            token,_ = Token.objects.get_or_create(user=user)
            return Response({'token':token.key},status=status.HTTP_200_OK)
            
    
    
class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer   
    permission_classes = []

    
class ProductView(ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter] 
    filterset_fields = ['price', 'created_at', 'category'] 
    
    search_fields = ['price', 'created_at','name']    
    permission_classes = []
    
class CardItemView(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    
    permission_classes = []
    
class OrderView(ModelViewSet):
    queryset = Order.objects.all().order_by('id')
    serializer_class = orderSerializer
    permission_classes = [DjangoModelPermissions,IsAuthenticated]   
    filterset_fields = ['quantity','price']
    filter_backends = [filters.SearchFilter]
    search_fields = ['quantity','price'] 
   
   
class OrderItemView(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [DjangoModelPermissions,IsAuthenticated]
    
class PaymentView(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [DjangoModelPermissions,IsAuthenticated]  
    
    
 
