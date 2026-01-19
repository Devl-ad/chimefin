from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .form import CreateTXSBForm, CreateTXInForm
from .models import Transactions
from django.http import JsonResponse
from django.db import transaction
import json


@login_required
def dashboard(request):

    return render(request, "user/dashboard.html")


@login_required
def transactions_view(request):
    user = request.user
    transactions = Transactions.objects.filter(sender=user).order_by("-date")

    return render(request, "user/transactions.html", {"transactions": transactions})


@login_required
def card_view(request):
    return render(request, "user/cards.html")


@login_required
def local_transfer(request):
    user = request.user

    if request.method == "POST":
        form = CreateTXSBForm(request.POST)

        if not form.is_valid():
            print(form.errors)
            return render(request, "user/localtransfer.html", {"form": form})

        pin = form.cleaned_data.get("pin")
        amount = form.cleaned_data.get("amount")

        if user.security_pin != pin:
            print("PIN")
            messages.error(request, "Invalid security PIN")
            return redirect("localtransfer")

        if user.balance < amount:
            print("INSS")
            messages.error(request, "Transaction failed: Insufficient funds")
            return redirect("localtransfer")

        with transaction.atomic():
            tx = form.save(commit=False)
            tx.sender = user
            tx.save()

            user.balance -= amount
            user.save(update_fields=["balance"])

        messages.success(
            request, f"Transaction of {amount} has been initiated and is under review"
        )
        print("nicee")
        return redirect("transaction-logs")

    else:
        form = CreateTXSBForm()

    return render(request, "user/localtransfer.html", {"form": form})


@login_required
def inter_transfer(request):
    user = request.user
    form = CreateTXSBForm()
    return render(request, "user/intertransfer.html", {"form": form})


@login_required
def inter_transfer_process(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON payload"}, status=400)

    form = CreateTXInForm(data)

    if not form.is_valid():
        return JsonResponse(
            {
                "errors": form.errors,  # Django error dict
            },
            status=400,
        )

    user = request.user
    pin = form.cleaned_data["pin"]
    amount = form.cleaned_data["amount"]

    if user.security_pin != pin:
        return JsonResponse(
            {"error": "Invalid security PIN"},
            status=400,
        )

    if user.balance < amount:
        return JsonResponse(
            {"error": "Insufficient balance"},
            status=400,
        )

    with transaction.atomic():
        tx = form.save(commit=False)
        tx.sender = user
        tx.save()

        user.balance -= amount
        user.save(update_fields=["balance"])

    return JsonResponse(
        {
            "success": True,
            "message": f"A wire transfer of {amount} has been initiated and is under review",
        },
        status=200,
    )


@login_required
def deposit_view(request):
    return render(request, "user/dash_deposits.html")


@login_required
def loan_view(request):
    return render(request, "user/loan.html")


@login_required
def account_view(request):
    return render(request, "user/account.html")
