from django.contrib.auth.decorators import login_required
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .forms import Login
from .models import Balance, Transaction
from .serializers import BalanceSerializer, TransactionSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

from .utils import get_user_transactions


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("start_page")

        return render(request, "login.html", context={
            'form': form,
            'is_valid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('login')


@login_required
def start_page(request):
    user = request.user

    balance = get_object_or_404(Balance, user=user).amount / 100
    transactions = get_user_transactions(user)

    context = {
        'balance': balance,
        'transactions': transactions,
    }

    return render(request, 'index.html', context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_balance(request):
    balance = get_object_or_404(Balance, user=request.user)

    return Response({'balance_rub': balance.amount / 100}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='post',
    request_body=BalanceSerializer,
    responses={
        status.HTTP_200_OK: BalanceSerializer,
        status.HTTP_400_BAD_REQUEST: 'Bad Request'
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def deposit(request):
    serializer = BalanceSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    amount = serializer.validated_data['amount']
    user = request.user

    balance = get_object_or_404(Balance, user=user)
    balance.amount += amount
    balance.save()

    Transaction.objects.create(sender=user, receiver=user, amount=amount)

    serialized_data = serializer.data
    serialized_data['user_id'] = user.id
    serialized_data['new_balance'] = balance.amount

    return Response(serialized_data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='post',
    request_body=TransactionSerializer,
    responses={
        status.HTTP_200_OK: TransactionSerializer,
        status.HTTP_400_BAD_REQUEST: 'Bad Request'
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def transfer(request):
    serializer = TransactionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    receiver_id = serializer.validated_data['receiver']['id']
    amount = serializer.validated_data['amount']
    receiver = get_object_or_404(User, id=receiver_id)
    sender = request.user

    if receiver_id == sender.id:
        return Response({'error': 'Одинаковые пользователи в Отправителе и Получателе'}, status=status.HTTP_200_OK)

    try:
        sender_balance = get_object_or_404(Balance, user=sender)
    except Balance.DoesNotExist:
        sender_balance = Balance.objects.create(user=request.user, amount=0)

    try:
        receiver_balance = get_object_or_404(Balance, user=receiver)
    except Balance.DoesNotExist:
        receiver_balance = Balance.objects.create(user=receiver, amount=0)

    if sender_balance.amount < amount:
        return Response({'error': 'Недостаточно средств у Отправителя'}, status=status.HTTP_200_OK)

    sender_balance.amount -= amount
    receiver_balance.amount += amount
    sender_balance.save()
    receiver_balance.save()

    Transaction.objects.create(sender=request.user, receiver=receiver, amount=amount)

    serialized_data = serializer.data
    serialized_data['sender_id'] = sender.id
    serialized_data['new_sender_balance'] = sender_balance.amount
    serialized_data['new_receiver_balance'] = receiver_balance.amount

    return Response(serialized_data, status=status.HTTP_200_OK)
