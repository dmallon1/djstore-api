from rest_framework import viewsets, status, mixins
from store.models import Product, Order, ProductInstance
from store.serializers import ProductSerializer, OrderSerializer, ProductInstanceSerializer
from rest_framework.response import Response
import stripe
import uuid
import requests
from store.utils import generate_random_six_character_string
from rest_framework.views import APIView
from rest_framework.response import Response


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductInstanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductInstance.objects.all()
    serializer_class = ProductInstanceSerializer


class OrderViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request):
        # validate captcha

        # call stripe api and update the order with the stripe id
        name = request.data['first_name'] + " " + request.data['last_name']
        charge_or_exception = create_charge(request.data['total'], request.data['card_token'], name)
        if isinstance(charge_or_exception, Exception):
            print(charge_or_exception) # TODO use logger instead
            return Response({"detail":"issue with stripe"}, status=status.HTTP_400_BAD_REQUEST)
        request.data['stripe_id'] = charge_or_exception["id"]

        # call gooten api and update the order with the gooten id
        resp = create_gooten_order(request.data)
        if resp.status_code is not 201:
            # TODO I probbaly should automatically refund the person or send myself
            # an email to take action if this ever happens
            print(resp.json())
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
            # TODO at this point too, if this fails here, we have issues
            # need to sound an alarm
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

        # return order number
        return Response({"detail": order_num}, status=status.HTTP_200_OK)


def create_charge(total, card_token, name):
    stripe.api_key = "sk_test_iWDVTESjjHJELulceKZ22o8n00CgpRftmA"

    total = round(total * 100)

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

    return charge


def create_gooten_order(data):
    url = "https://api.print.io/api/v/5/source/api/orders/"

    querystring = {"recipeid":"616ee03b-655d-4e00-a608-4dffc10cfe60"}
    billing_key = "qWl9uozF/jDzoZUU4hO6XwM3g4ucccWPYOEp1uhP3do="

    # have to create items list to insert below
    items = []
    for instance in data['product_instances']:
        item = {
            "Quantity": instance['quantity'],
            "SKU": instance['sku'],
            "ShipCarrierMethodId": 1,
        }
        items.append(item)

    payload = {
        "ShipToAddress": {
            "FirstName": data['first_name'],
            "LastName": data['last_name'],
            "Line1": data['address1'],
            "Line2": data.get('address2'),
            "City": data['city'],
            "State": data['state'],
            "CountryCode": "US",
            "PostalCode": data['zip_code'],
            "IsBusinessAddress": False,
            "Phone": "1234567890",
            "Email": data['email']
        },
        "BillingAddress": {
            "FirstName": data['first_name'],
            "LastName": data['last_name'],
            "Line1": data['address1'],
            "Line2": data.get('address2'),
            "City": data['city'],
            "State": data['state'],
            "CountryCode": "US",
            "PostalCode": data['zip_code'],
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


class OrderLookup(APIView):
    """
    View to lookup orders.
    """

    def post(self, request, format=None):
        """
        Returns order information.
        """

        try:
            order = Order.objects.get(dj_order_id=request.data.get('order_id'), zip_code=request.data.get('zip_code'))
        except Order.DoesNotExist:
            return Response({"detail": "not found"}, status=404)

        product_serializer = ProductInstanceSerializer(order.product_instances, many=True)

        data = {
            "order_id": order.dj_order_id,
            "status": order.status,
            "tracking_number": order.tracking_number,
            "product_instances": product_serializer.data,
            "total": order.total,
        }

        return Response(data)
