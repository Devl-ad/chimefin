from django.shortcuts import render


def home_page(request):
    return render(request, "index.html")


def why_us(request):
    return render(request, "why.html")


def credit_card(request):
    return render(request, "credit-card.html")


def current_account(request):
    return render(request, "current-account.html")


def savings_acct(request):
    return render(request, "savings-acct.html")


def personal_loan(request):
    return render(request, "personal-loan.html")


def mortgages_page(request):
    return render(request, "mortgages.html")


def personal_insurance(request):
    return render(request, "personal-insurance.html")


def dedeposite_page(request):
    return render(request, "deposit-info.html")


def foreign_drafts(request):
    return render(request, "foreign-drafts.html")


def interest_checking(request):
    return render(request, "interest-checking.html")


def Tele_banking(request):
    return render(request, "tele-banking.html")


def invest_benefit(request):
    return render(request, "invest-benefits.html")


def mma(request):
    return render(request, "money-market-account.html")


def small_bussiness(request):
    return render(request, "small-business.html")


def contact_us(request):
    return render(request, "contact-us.html")
