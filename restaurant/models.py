from datetime import datetime

from django.db import models


# Create your models here.
class Booking(models.Model):
    first_name = models.CharField(max_length=200, default='First name')
    last_name = models.CharField(max_length=200, default='Last name')
    guest_number = models.IntegerField()
    comment = models.CharField(max_length=1000)
    reservation_date = models.DateField()
    reservation_slot = models.SmallIntegerField(default=10)
    BALCONY = 'Balcony'
    NEAR_WINDOW = 'near_window'
    CONCEPT_HAPPY_BIRTHDAY = 'concept_happy_birthday'
    CELEBRATION = 'wedding_celebration'
    FLOOR_1 = 'floor_1'
    FLOOR_2 = 'floor_2'
    FLOOR_3 = 'floor_3'
    TAG_CHOICES = [
        (BALCONY, 'Balcony'),
        (NEAR_WINDOW, 'Near Window'),
        (CONCEPT_HAPPY_BIRTHDAY, 'Concept Happy Birthday'),
        (CELEBRATION, 'Celebration'),
        (FLOOR_1, 'Floor 1'),
        (FLOOR_2, 'Floor 2'),
        (FLOOR_3, 'Floor 3'),
    ]

    tags = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


# Add code to create Menu model
class Menu(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField(null=False)
    menu_item_description = models.TextField(max_length=1000, default='')

    def __str__(self):
        return self.name

