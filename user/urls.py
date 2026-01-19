from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("transaction-logs/", views.transactions_view, name="transaction-logs"),
    path("cards-view/", views.card_view, name="card"),
    path("local-transfer/", views.local_transfer, name="localtransfer"),
    path("inter-transfer/", views.inter_transfer, name="inter-transfer"),
    path(
        "inter-transfer-process/",
        views.inter_transfer_process,
        name="process-int-transfer",
    ),
    path("deposit/", views.deposit_view, name="deposit"),
    path("loan/", views.loan_view, name="loan"),
    path("account-overview/", views.account_view, name="account-overview"),
]
