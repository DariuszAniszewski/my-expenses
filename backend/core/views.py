from collections import defaultdict
from calendar import monthrange

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

# Create your views here.
from django.views.generic.dates import timezone_today

from core.models import Expense, Income


@staff_member_required
def index(request):
    data = {
        "page": "home"
    }
    return render(request, "index.html", data)


def view_year(request, year):
    all_expenses = Expense.objects.all().order_by('date')
    total = 0
    paid_with_credit_card_total = 0

    categories = defaultdict(lambda: {"items": [], "total": 0})
    subcategories = defaultdict(lambda: {"items": [], "total": 0})
    places = defaultdict(lambda: {"items": [], "total": 0})

    # calculate_totals first
    for expense in all_expenses:
        total += expense.total
        if expense.paid_with_credit_card:
            paid_with_credit_card_total += expense.total

    for expense in all_expenses:
        places[expense.place.name]["name"] = expense.place.name
        places[expense.place.name]["total"] += expense.total
        places[expense.place.name]["percentage"] = round(100 * places[expense.place.name]["total"] / total)
        for item in expense.items():
            categories[item.category.name]["name"] = item.category.name
            categories[item.category.name]["items"].append(item)
            categories[item.category.name]["total"] += item.amount
            categories[item.category.name]["percentage"] = round(100 * categories[item.category.name]["total"] / total)
            if item.subcategory:
                subcategories[item.subcategory.name]["name"] = str(item.subcategory)
                subcategories[item.subcategory.name]["items"].append(item)
                subcategories[item.subcategory.name]["total"] += item.amount
                subcategories[item.subcategory.name]["percentage"] = round(100 * subcategories[item.subcategory.name]["total"] / total)

    categories = sorted(dict(categories).values(), key=lambda i: -i["total"])
    subcategories = sorted(dict(subcategories).values(), key=lambda i: -i["total"])
    places = sorted(dict(places).values(), key=lambda i: -i["total"])

    income_total = sum([income.amount for income in Income.objects.all()])
    left = income_total - total
    today = timezone_today()
    days_in_month = monthrange(today.year, today.month)[1]

    data = {
        "page": year,
        "total_income": income_total,
        "expenses": all_expenses,
        "categories": categories,
        "subcategories": subcategories,
        "paid_with_credit_card": paid_with_credit_card_total,
        "places": places,
        "total": total,
        "left": left,
        "left_per_day": left / 31,
        "days_in_month": days_in_month,
        "today": today,
        "days_left": days_in_month - today.day
    }
    return render(request, "expenses.html", data)
