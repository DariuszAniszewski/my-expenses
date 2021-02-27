from django.contrib import admin

# Register your models here.
from core.models import Category, SubCategory, Place, Expense, ExpenseItem, Income


class IncomeAdmin(admin.ModelAdmin):
    list_display = ["date", "amount", 'category', "subcategory"]
    readonly_fields = ('date_year', 'date_month', 'date_day')


class PlaceAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    ordering = ["name"]


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    ordering = ["name"]


class SubCategoryAdmin(admin.ModelAdmin):
    search_fields = ["name", "category__name"]
    ordering = ["category__name", "name"]


class ExpenseItemInlineAdmin(admin.StackedInline):
    model = ExpenseItem
    autocomplete_fields = ["category", "subcategory"]

    def get_extra(self, request, obj=None, **kwargs):
        return 0 if obj else 1


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ["date", "place", 'total', "paid_with_credit_card"]
    inlines = [ExpenseItemInlineAdmin]
    readonly_fields = ('total', 'date_year', 'date_month', 'date_day')
    ordering = ["-date"]
    autocomplete_fields = ["place"]


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Income, IncomeAdmin)
admin.site.register(Expense, ExpenseAdmin)
