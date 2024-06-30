# Generated by Django 5.0.3 on 2024-03-28 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image_url',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(blank=True, null=True, upload_to='img/products'),
        ),
    ]
