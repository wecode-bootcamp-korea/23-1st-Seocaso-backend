import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Seocaso.settings")
django.setup()

from cafes.models import Cafe, Menu

CSV_PATH_CAFES = 'menus.csv'

with open(CSV_PATH_CAFES) as in_file:
    data_reader = csv.reader(in_file)
    # next(data_reader)
    next(data_reader, None)

    # for row in data_reader:
    #     name                 = row[1]
    #     address              = row[2]
    #     hours                = row[3]
    #     number               = row[4]
    #     information          = row[5]
    #     background_image_url = row[6]
    #     poster_url           = row[7]

    #     Cafe.objects.create(name=name, address=address, hours=hours, number=number, information=information, background_image_url=background_image_url, poster_url=poster_url)

    for row in data_reader:
        cafe_id   = row[1]
        name      = row[2]
        price     = row[3]
        image_url = row[4]

        Menu.objects.create(cafe=Cafe.objects.get(id=cafe_id), name=name, price=price, image_url=image_url)