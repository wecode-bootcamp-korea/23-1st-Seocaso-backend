# Generated by Django 3.2.6 on 2021-08-05 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_email'),
        ('cafes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CafeCollection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'db_table': 'cafes_colloections',
            },
        ),
        migrations.CreateModel(
            name='CafeList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cafe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cafes.cafe')),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cafes.cafecollection')),
            ],
            options={
                'db_table': 'cafes_lists',
            },
        ),
    ]
