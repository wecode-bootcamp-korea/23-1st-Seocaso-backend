# Generated by Django 3.2.6 on 2021-08-02 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafes', '0002_cafe_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cafe',
            name='address',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='cafe',
            name='stars',
            field=models.DecimalField(decimal_places=1, max_digits=2),
        ),
    ]