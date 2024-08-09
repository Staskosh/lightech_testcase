from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User


class Balance(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='balances',
        verbose_name='Пользователь',
    )
    amount = models.DecimalField(
        'Сумма',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = 'Счет'
        verbose_name_plural = 'Счета'

    def __str__(self):
        return f'{self.user.username} - {self.amount}'


class Transaction(models.Model):
    sender = models.ForeignKey(
        User,
        related_name='sent_transactions',
        on_delete=models.CASCADE,
        verbose_name='Отправитель',
    )
    receiver = models.ForeignKey(
        User,
        related_name='received_transactions',
        on_delete=models.CASCADE,
        verbose_name='Получатель',
    )
    amount = models.DecimalField(
        'Сумма',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField('Дата и время создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

    def __str__(self):
        return f'{self.sender.username} - {self.amount}'
