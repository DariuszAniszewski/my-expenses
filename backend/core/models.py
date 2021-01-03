import uuid

from django.db import models


class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Place(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name
