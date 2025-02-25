# Generated by Django 2.2.7 on 2019-11-06 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_auto_20190922_0117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product_quantity_instances',
        ),
        migrations.AddField(
            model_name='order',
            name='product_instances',
            field=models.ManyToManyField(to='store.ProductInstance'),
        ),
        migrations.AddField(
            model_name='productinstance',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.FloatField(),
        ),
        migrations.DeleteModel(
            name='ProductQuantityInstance',
        ),
    ]
