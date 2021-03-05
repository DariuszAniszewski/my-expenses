from collections import defaultdict
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.views.generic.dates import timezone_today
from core.models import Expense, Income


@staff_member_required
def index(request):
    today = timezone_today()
    return redirect("month", today.year, today.month)


def view_month(request, year, month):
    all_expenses = Expense.objects.filter(date_year=year, date_month=month).order_by('-date')
    all_income = Income.objects.filter(date_year=year, date_month=month).order_by('-date')

    data = __do_all_calculations(all_expenses, all_income)
    return render(request, "expenses.html", data)


def view_year(request, year):
    all_expenses = Expense.objects.filter(date_year=year).order_by('-date')
    all_income = Income.objects.filter(date_year=year).order_by('-date')

    data = __do_all_calculations(all_expenses, all_income)
    return render(request, "expenses.html", data)


def __do_all_calculations(all_expenses, all_income):
    total = 0
    paid_with_credit_card_total = 0
    categories = defaultdict(lambda: {"items": [], "total": 0})
    subcategories = defaultdict(lambda: {"items": [], "total": 0})
    places = defaultdict(lambda: {"items": [], "total": 0})
    days = defaultdict(lambda: {"items": [], "total": 0})
    # calculate_totals first
    for expense in all_expenses:
        total += expense.total
        if expense.paid_with_credit_card:
            paid_with_credit_card_total += expense.total
    for expense in all_expenses:
        places[expense.place.name]["name"] = expense.place.name
        places[expense.place.name]["total"] += expense.total
        places[expense.place.name]["percentage"] = round(100 * places[expense.place.name]["total"] / total)
        days[expense.date]["name"] = expense.date
        days[expense.date]["total"] += expense.total
        days[expense.date]["percentage"] = round(100 * days[expense.date]["total"] / total)
        for item in expense.items():
            categories[item.category.name]["name"] = item.category.name
            categories[item.category.name]["items"].append(item)
            categories[item.category.name]["total"] += item.amount
            categories[item.category.name]["percentage"] = round(100 * categories[item.category.name]["total"] / total)
            if item.subcategory:
                subcategories[item.subcategory.name]["name"] = str(item.subcategory)
                subcategories[item.subcategory.name]["items"].append(item)
                subcategories[item.subcategory.name]["total"] += item.amount
                subcategories[item.subcategory.name]["percentage"] = round(
                    100 * subcategories[item.subcategory.name]["total"] / total)
    categories = sorted(dict(categories).values(), key=lambda i: -i["total"])
    subcategories = sorted(dict(subcategories).values(), key=lambda i: -i["total"])
    places = sorted(dict(places).values(), key=lambda i: -i["total"])
    days = sorted(dict(days).values(), key=lambda i: i["name"])
    income_total = sum([income.amount for income in all_income])
    left = income_total - total
    data = {
        "total_income": income_total,
        "expenses": all_expenses,
        "categories": categories,
        "subcategories": subcategories,
        "paid_with_credit_card": paid_with_credit_card_total,
        "places": places,
        "days": days,
        "total": total,
        "left": left,
    }
    return data
