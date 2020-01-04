from rest_framework import serializers
from store.models import Product, Order, ProductInstance, CartProductInstance


class ProductInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInstance
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    product_instances = ProductInstanceSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = '__all__'


class CartProductInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProductInstance
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    cart_product_instances = CartProductInstanceSerializer(many=True)
    class Meta:
        model = Order
        fields = ('email', 'first_name', 'last_name', 'address1', 'address2',
            'city', 'state', 'zip_code', 'card_token', 'captcha_token', 'total',
            'cart_product_instances', 'stripe_id', 'gooten_id', 'dj_order_id')

    def create(self, validated_data):
        cart_product_list = validated_data.pop('cart_product_instances')
        cart_product_refs = []
        for cart_product in cart_product_list:
            obj, _ = CartProductInstance.objects.get_or_create(**cart_product)
            cart_product_refs.append(obj)

        order = Order.objects.create(**validated_data)
        order.cart_product_instances.set(cart_product_refs)
        return order
