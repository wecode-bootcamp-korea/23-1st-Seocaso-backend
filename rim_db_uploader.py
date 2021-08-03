import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Seocaso.settings")
django.setup()

from users.models import User

CSV_PATH_USERS = './users.csv'

with open(CSV_PATH_USERS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        email    = row[1]
        password = row[2]
        nickname = row[3]

        User.objects.create(email=email, password=password, nickname=nickname)