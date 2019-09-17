from rest_framework import serializers
from store.models import Product, Order, ProductQuantityInstance, ProductInstance


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInstance
        fields = '__all__'

class ProductQuantityInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductQuantityInstance
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    product_quantity_instances = ProductQuantityInstanceSerializer(many=True)
    class Meta:
        model = Order
        fields = ('email', 'first_name', 'last_name', 'address1', 'address2',
            'city', 'state', 'zip', 'card_token', 'captcha_token', 'total',
            'product_quantity_instances', 'gooten_id', 'dj_order_id')

    def create(self, validated_data):
        product_list = validated_data.pop('product_quantity_instances')
        product_refs = []
        for product in product_list:
            obj, _ = ProductQuantityInstance.objects.get_or_create(**product)
            product_refs.append(obj)

        order = Order.objects.create(**validated_data)
        order.product_quantity_instances.set(product_refs)
        return order
