from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_page, name="home"),
    path("why-us/", views.why_us, name="why-us"),
    path("credit-card/", views.credit_card, name="cc"),
    path("current-accounts/", views.current_account, name="ca"),
    path("savings-account/", views.savings_acct, name="savingsacct"),
    path("personal-loan/", views.personal_loan, name="personaloan"),
    path("mortgages/", views.mortgages_page, name="mortgages"),
    path("personal-insurance/", views.personal_insurance, name="personal-insurance"),
    path("deposit-info/", views.dedeposite_page, name="deposit-info"),
    path("foreign-drafts/", views.foreign_drafts, name="foreign-drafts"),
    path("interest-checking/", views.interest_checking, name="intrest-checking"),
    path("tele-banking/", views.Tele_banking, name="tele-banking"),
    path("invest-benefits/", views.invest_benefit, name="invest-benefits"),
    path("money-market-account/", views.mma, name="mma"),
    path("small-business/", views.small_bussiness, name="small-business"),
    path("contact-us/", views.contact_us, name="contact-us"),
]
