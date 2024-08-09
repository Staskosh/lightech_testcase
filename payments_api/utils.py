from django.db.models import Q
from payments_api.models import Transaction


def get_user_transactions(user):
    transactions = Transaction.objects.select_related('sender', 'receiver')\
        .filter(Q(sender=user) | Q(receiver=user)).order_by('-created_at')

    return transactions
