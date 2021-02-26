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
    name = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.category} / {self.name}"

    class Meta:
        unique_together = ["category", "name"]


class Place(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Expense(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    date = models.DateField()
    place = models.ForeignKey(Place, on_delete=models.PROTECT)
    date_year = models.IntegerField(editable=False, null=True)
    date_month = models.IntegerField(editable=False, null=True)
    date_day = models.IntegerField(editable=False, null=True)
    paid_with_credit_card = models.BooleanField(default=False)

    def _get_total(self) -> int:
        items = ExpenseItem.objects.filter(expense=self)
        return sum([i.amount for i in items])

    total = property(_get_total)

    def items(self):
        return self.expenseitem_set.all()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.date_year = self.date.year
        self.date_month = self.date.month
        self.date_day = self.date.day
        super().save(force_insert, force_update, using, update_fields)


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
    date_year = models.IntegerField(editable=False, null=True)
    date_month = models.IntegerField(editable=False, null=True)
    date_day = models.IntegerField(editable=False, null=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.date_year = self.date.year
        self.date_month = self.date.month
        self.date_day = self.date.day
        super().save(force_insert, force_update, using, update_fields)
