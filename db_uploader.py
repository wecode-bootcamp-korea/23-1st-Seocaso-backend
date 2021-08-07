import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Seocaso.settings")
django.setup()

from cafes.models import *
from users.models import User

CSV_PATH_CAFES = 'cafes.csv'

with open(CSV_PATH_CAFES) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Cafe.objects.create(
            name = row[1],
            address = row[2],
            business_hours = row[3],
            phone_number = row[4],
            description = row[5],
            main_image_url = row[6]
        )

CSV_PATH_CAFES = 'cafe_images.csv'

with open(CSV_PATH_CAFES) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        CafeImage.objects.create(
            image_url = row[1],
            cafe = Cafe.objects.get(id=row[2])
        )        

CSV_PATH_CAFES = 'menus.csv'

with open(CSV_PATH_CAFES) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Menu.objects.create(
            cafe = Cafe.objects.get(id=row[1]),
            name = row[2],
            price = row[3],
            image_url = row[4]
        )
