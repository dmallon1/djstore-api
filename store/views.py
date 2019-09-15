from django.shortcuts import render
from rest_framework import viewsets
from store.models import Product, Order, ProductInstance
from store.serializers import ProductSerializer, OrderSerializer, ProductInstanceSerializer
from rest_framework import mixins
from rest_framework.response import Response
import stripe
import uuid
import requests


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductInstanceViewSet(viewsets.ModelViewSet):
    queryset = ProductInstance.objects.all()
    serializer_class = ProductInstanceSerializer


class OrderViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request):
        # validate captcha

        # call stripe api
        name = request.data['first_name'] + " " + request.data['last_name']
        create_charge(request.data['total'], request.data['card_token'], name)

        # call gooten api
        create_gooten_order(request.data)

        # update the order with the gooten id
        # return success url with order number (might need validation around this)
        return super(OrderViewSet, self).create(request)


def create_charge(total, card_token, name):
    stripe.api_key = "sk_test_iWDVTESjjHJELulceKZ22o8n00CgpRftmA"

    charge = stripe.Charge.create(
        amount=total,
        currency="usd",
        description="Charge for " + name, # this has to potential to change
        source=card_token,
        idempotency_key=str(uuid.uuid4()),
    )

def create_gooten_order(data):
    url = "https://api.print.io/api/v/5/source/api/orders/"

    querystring = {"recipeid":"616ee03b-655d-4e00-a608-4dffc10cfe60"}
    billing_key = "qWl9uozF/jDzoZUU4hO6XwM3g4ucccWPYOEp1uhP3do="

    # have to create items list to insert below
    items = []
    for instance in data['product_quantity_instances']:
        product_instance = ProductInstance.objects.get(id=instance['product_instance'])
        item = {
            "Quantity": instance['quantity'],
            "SKU": product_instance.sku,
            "ShipCarrierMethodId": 1,
        }
        items.append(item)

    payload = {
        "ShipToAddress": {
            "FirstName": data['first_name'],
            "LastName": data['last_name'],
            "Line1": data['address1'],
            "Line2": data['address2'],
            "City": data['city'],
            "State": data['state'],
            "CountryCode": "US",
            "PostalCode": data['zip'],
            "IsBusinessAddress": False,
            "Phone": "1234567890",
            "Email": data['email']
        },
        "BillingAddress": {
            "FirstName": data['first_name'],
            "LastName": data['last_name'],
            "Line1": data['address1'],
            "Line2": data['address2'],
            "City": data['city'],
            "State": data['state'],
            "CountryCode": "US",
            "PostalCode": data['zip'],
            "IsBusinessAddress": False,
            "Phone": "1234567890",
            "Email": data['email']
        },
        "IsInTestMode": True,
        "Items": items,
        "Payment": {
            "PartnerBillingKey": billing_key
        },
        # "Meta":{ this could be useful
        #     "key1":"value"
        # }
        # could add another source id for impotency
    }

    headers = {'content-type': 'application/json'}

    response = requests.post(url, json=payload, headers=headers, params=querystring)

    print(response.text)
