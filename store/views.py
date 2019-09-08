from django.shortcuts import render
from rest_framework import viewsets
from django.http import HttpResponse
from store.models import Product
from store.serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
