# Generated by Django 3.2.6 on 2021-08-03 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cafes', '0005_auto_20210803_1133'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('price', models.CharField(max_length=45)),
                ('image_url', models.URLField(max_length=1000)),
                ('cafe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cafes.cafe')),
            ],
            options={
                'db_table': 'menus',
            },
        ),
    ]