from django.db import models


class ShirtSize(models.Model):
    # s,m,l,xl,xxl
    size = models.CharField(max_length=3)

    def __str__(self):
        return self.size


class Product(models.Model):
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=1024)
    price = models.PositiveIntegerField()
    picture_url = models.CharField(max_length=256)
    available_sizes = models.ManyToManyField(ShirtSize)

    def __str__(self):
        return self.title


class ProductInstance(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    size = models.ForeignKey(ShirtSize, on_delete=models.PROTECT)
    sku = models.TextField(max_length=512)

    def __str__(self):
        return self.product.title + " | " + self.size.size


class ProductQuantityInstance(models.Model):
    product_instance = models.ForeignKey(ProductInstance, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return "[" + str(self.quantity) + "] " + self.product_instance.product.title + " - " + self.product_instance.size.size


class Order(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    address1 = models.CharField(max_length=128)
    address2 = models.CharField(max_length=128, blank=True, null=True)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=2)
    zip = models.PositiveIntegerField()
    card_token = models.CharField(max_length=256)
    captcha_token = models.CharField(max_length=512)
    product_quantity_instances = models.ManyToManyField(ProductQuantityInstance)
    total = models.PositiveIntegerField()
    stripe_id = models.CharField(max_length=128, null=True, blank=True)
    gooten_id = models.CharField(max_length=128, null=True, blank=True)
    dj_order_id = models.CharField(max_length=6, unique=True, default="yo")

    def __str__(self):
        return self.first_name + " " + self.last_name
