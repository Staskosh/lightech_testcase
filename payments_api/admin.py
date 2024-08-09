from django.contrib import admin


from .models import Balance, Transaction


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    search_fields = [
        'user',
    ]
    list_display = [
        'user',
        'amount',
    ]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    search_fields = [
        'sender',
    ]
    list_display = [
        'sender',
        'receiver',
        'amount',
        'created_at',
    ]
