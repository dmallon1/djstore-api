from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=1024)
    price = models.PositiveIntegerField()
    picture_url = models.CharField(max_length=256)
    available_sizes = models.CharField(max_length=64)
    # "s,m,l,xl,xxl"

    def __str__(self):
        return self.title
