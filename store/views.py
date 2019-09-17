from rest_framework import viewsets, status, mixins
from store.models import Product, Order, ProductInstance
from store.serializers import ProductSerializer, OrderSerializer, ProductInstanceSerializer
from rest_framework.response import Response
import stripe
import uuid
import requests
from store.utils import generate_random_six_character_string


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
        error_or_none = create_charge(request.data['total'], request.data['card_token'], name)
        if error_or_none:
            return Response({"detail":"issue with stripe"}, status=status.HTTP_400_BAD_REQUEST)

        # call gooten api and update the order with the gooten id
        resp = create_gooten_order(request.data)
        if resp.status_code is not 201:
            return Response({"detail":"issue with gooten"}, status=status.HTTP_400_BAD_REQUEST)
        request.data['gooten_id'] = resp.json()['Id']

        # generate order number and add to order (making sure order_num is not already being used)
        order_num = generate_random_six_character_string()
        while Order.objects.filter(dj_order_id=order_num).count() > 0:
            order_num = generate_random_six_character_string()
        request.data['dj_order_id'] = order_num

        # validate and save data if appropriate
        serializer = OrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

        # return order number
        return Response({"detail": order_num}, status=status.HTTP_200_OK)


def create_charge(total, card_token, name):
    stripe.api_key = "sk_test_iWDVTESjjHJELulceKZ22o8n00CgpRftmA"

    try:
        charge = stripe.Charge.create(
            amount=total,
            currency="usd",
            description="Charge for " + name, # this has to potential to change
            source=card_token,
            idempotency_key=str(uuid.uuid4()),
        )
    except Exception as e:
        return e

    return None


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

    return response
