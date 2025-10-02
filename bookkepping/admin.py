from django.contrib import admin
from .models import Account, Transaction, LedgerEntry


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'balance')
    list_filter = ('type',)
    search_fields = ('name',)


class LedgerEntryInline(admin.TabularInline):
    model = LedgerEntry
    extra = 1


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'description')
    date_hierarchy = 'date'
    search_fields = ('description',)
    inlines = [LedgerEntryInline]
    
    def save_model(self, request, obj, form, change):
        # Skip validation for admin saves since entries are handled separately
        obj.save()


@admin.register(LedgerEntry)
class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'account', 'debit', 'credit')
    list_filter = ('account__type',)
    search_fields = ('transaction__description', 'account__name')
