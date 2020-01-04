from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=1024)
    price = models.PositiveIntegerField()
    picture_url = models.CharField(max_length=256)

    def __str__(self):
        return self.title


class ProductInstance(models.Model):
    SIZE_CHOICES = [
        ('s', 'small'),
        ('m', 'medium'),
        ('l', 'large'),
        ('xl', 'extra large'),
        ('xxl', 'double extra large'),
        ('xxxl', 'triple extra large'),
    ]

    product = models.ForeignKey(Product, related_name='product_instances', on_delete=models.PROTECT)
    size = models.CharField(max_length=4, choices=SIZE_CHOICES)
    sku = models.TextField(max_length=512)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return "[" + str(self.quantity) + "] " + self.product.title + " | " + self.size


class Order(models.Model):
    STATUS_CHOICES = [
        ('p', 'processing'),
        ('s', 'shipped'),
        ('d', 'delivered'),
    ]

    email = models.EmailField()
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    address1 = models.CharField(max_length=128)
    address2 = models.CharField(max_length=128, blank=True, null=True)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=10)
    card_token = models.CharField(max_length=256)
    captcha_token = models.CharField(max_length=512)
    product_instances = models.ManyToManyField(ProductInstance)
    total = models.FloatField()
    stripe_id = models.CharField(max_length=128, null=True, blank=True)
    gooten_id = models.CharField(max_length=128, null=True, blank=True)
    dj_order_id = models.CharField(max_length=6, unique=True, default="yo")

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='p')
    tracking_number = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name
