# Generated by Django 3.2.6 on 2021-08-04 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cafes', '0001_initial'),
        ('users', '0001_initial'),
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.review')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.user')),
            ],
            options={
                'db_table': 'review_likes',
            },
        ),
        migrations.CreateModel(
            name='CafeLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cafe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cafes.cafe')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.user')),
            ],
            options={
                'db_table': 'cafe_likes',
            },
        ),
    ]
