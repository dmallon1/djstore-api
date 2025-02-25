# Generated by Django 2.2.5 on 2019-09-15 19:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20190913_0233'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productinstance',
            old_name='chosen_size',
            new_name='size',
        ),
        migrations.RemoveField(
            model_name='order',
            name='product_instances',
        ),
        migrations.RemoveField(
            model_name='productinstance',
            name='quantity',
        ),
        migrations.CreateModel(
            name='ProductQuantityInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('product_instance', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.ProductInstance')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='product_quantity_instances',
            field=models.ManyToManyField(to='store.ProductQuantityInstance'),
        ),
    ]
