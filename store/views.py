from django.shortcuts import render
from rest_framework import viewsets
from store.models import Product, Order
from store.serializers import ProductSerializer, OrderSerializer
from rest_framework import mixins


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request):
        print('yo')
        # validate captcha
        # make stripe api call
        # return success url with order number (might need validation around this)
        return super(OrderViewSet, self).create(request)
