from django.db import models
from account.models import Account


STATUS = (("PENDING", "PENDING"), ("SUCCESS", "SUCCESS"), ("DECLINED", "DECLINED"))


class InternationalDetails(models.Model):
    bic_code = models.CharField(max_length=20, null=True, blank=True)
    iban_number = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.country}"


class Transactions(models.Model):
    sender = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name="trans_sender"
    )

    bank_name = models.CharField(max_length=100, null=True, blank=True)
    invoiceRef = models.CharField(max_length=10)
    amount = models.IntegerField()
    purpose = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, default="PENDING", choices=STATUS)
    date = models.DateTimeField()
    route_num = models.CharField(max_length=100, null=True, blank=True)
    ben_name = models.CharField(max_length=100, null=True, blank=True)
    ben_acct = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    interDetail = models.ForeignKey(
        InternationalDetails, on_delete=models.CASCADE, null=True, blank=True
    )

    def format_balance(self):
        return "{:,}".format(self.amount)

    def __str__(self):
        return f"{self.sender.get_full_name()} -- {self.invoiceRef}"
