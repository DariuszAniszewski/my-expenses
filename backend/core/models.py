import uuid
from django.db import models


class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Place(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Expense(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    date = models.DateField()
    place = models.ForeignKey(Place, on_delete=models.PROTECT)

    def _get_total(self) -> int:
        items = ExpenseItem.objects.filter(expense=self)
        return sum([i.amount for i in items])

    total = property(_get_total)

    def items(self):
        return self.expenseitem_set.all()


class ExpenseItem(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT, blank=True, null=True)
    amount = models.IntegerField()
    notes = models.TextField(blank=True, null=True)


class Income(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    date = models.DateField()
    amount = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT, blank=True, null=True)
