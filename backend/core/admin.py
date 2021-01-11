from django.contrib import admin

# Register your models here.
from core.models import Category, SubCategory, Place, Expense, ExpenseItem, Income


class ExpenseItemInlineAdmin(admin.TabularInline):
    model = ExpenseItem

    def get_extra(self, request, obj=None, **kwargs):
        return 0 if obj else 1


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ["date", "place", 'total']
    inlines = [ExpenseItemInlineAdmin]
    readonly_fields = ('total',)


admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Place)
admin.site.register(Income)
admin.site.register(Expense, ExpenseAdmin)

