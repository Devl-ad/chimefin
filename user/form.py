from django import forms
from .models import Transactions, InternationalDetails
from baseapp import utils
from django.utils import timezone


class CreateTXSBForm(forms.ModelForm):

    purpose = forms.CharField()
    amount = forms.IntegerField()
    ben_name = forms.CharField()
    type = forms.CharField()
    bank_name = forms.CharField()
    pin = forms.CharField()
    ben_acct = forms.CharField()

    class Meta:
        model = Transactions
        fields = [
            "purpose",
            "amount",
            "pin",
            "ben_name",
            "bank_name",
            "type",
            "ben_acct",
        ]

    def __init__(self, *args, **kwargs):
        self.sender = kwargs.pop("sender", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        transaction = super().save(commit=False)

        transaction.sender = self.sender

        transaction.purpose = self.cleaned_data["purpose"]
        transaction.bank_name = self.cleaned_data["bank_name"]
        transaction.ben_name = self.cleaned_data["ben_name"]
        transaction.ben_acct = self.cleaned_data["ben_acct"]
        transaction.type = self.cleaned_data["type"]
        transaction.invoiceRef = utils.trans_code()
        transaction.amount = int(self.cleaned_data["amount"])

        transaction.date = timezone.now()

        if commit:
            transaction.save()
            self.sender.balance -= transaction.amount
            self.sender.save()

        return transaction


class CreateTXInForm(forms.ModelForm):

    ben_name = forms.CharField()

    ben_account_number = forms.CharField()

    bank_name = forms.CharField()

    bank_address = forms.CharField()

    amount = forms.IntegerField()

    purpose = forms.CharField()

    bic_code = forms.CharField()

    iban_number = forms.CharField()

    type = forms.CharField()

    country = forms.CharField()

    pin = forms.CharField()

    class Meta:
        model = Transactions
        fields = [
            "ben_name",
            "ben_account_number",
            "bank_name",
            "bank_address",
            "amount",
            "purpose",
            "bic_code",
            "iban_number",
            "type",
            "country",
            "pin",
        ]

    def __init__(self, *args, **kwargs):
        self.sender = kwargs.pop("sender", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        transaction = super().save(commit=False)

        transaction.sender = self.sender
        transaction.type = self.cleaned_data["type"]
        transaction.invoiceRef = utils.trans_code()
        transaction.date = timezone.now()

        transaction.purpose = self.cleaned_data["purpose"]
        transaction.bank_name = (
            f"{self.cleaned_data["bank_name"]}: {self.cleaned_data["bank_address"]}"
        )

        transaction.ben_acct = self.cleaned_data["ben_account_number"]

        details = InternationalDetails.objects.create(
            country=self.cleaned_data["country"],
            iban_number=self.cleaned_data["iban_number"],
            bic_code=self.cleaned_data["bic_code"],
        )

        transaction.interDetail = details

        if commit:
            transaction.save()

        return transaction
