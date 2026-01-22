from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    first_name = models.CharField(max_length=100)
    midle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    phone_number = models.CharField(max_length=100)
    date_of_birth = models.CharField(max_length=100)
    gender = models.CharField(max_length=50)

    address = models.CharField(max_length=100)
    occupation = models.CharField(
        max_length=100,
    )
    annual_salary_range = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    ssn = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    account_type = models.CharField(max_length=100, blank=True, null=True)

    balance = models.IntegerField(default=0)

    security_pin = models.CharField(max_length=100, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    ip_address = models.CharField(max_length=15, blank=True, null=True)

    profile_image = models.ImageField(upload_to="profile/", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def image_url(self):
        if self.profile_image:
            #
            return f"http://localhost:8000{self.profile_image.url}"
        else:
            return f"https://ui-avatars.com/api/?name={self.first_name} "

    def format_balance(self):
        return "{:,}".format(self.balance)

    def in_debt(self):
        if self.balance < 0:
            return True
        return False

    def __str__(self):
        return self.email

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    # def save(self, *args, **kwargs):
    #     # Perform custom logic before saving
    #     self.username = utils.gen_random_number()

    #     # Call parent save method
    #     super().save(*args, **kwargs)


# models.py


class Kyc(models.Model):
    user = models.OneToOneField(
        Account,
        related_name="user_kyc",
        on_delete=models.CASCADE,
    )

    # Personal Details

    title = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    dob = models.DateField()

    # Employment
    ssn = models.CharField(max_length=100)
    account_type = models.CharField(max_length=100)
    employment_type = models.CharField(max_length=100)
    income_range = models.CharField(max_length=100)

    # Address
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    # Next of Kin
    kin_name = models.CharField(max_length=255)
    kin_address = models.CharField(max_length=255)
    relationship = models.CharField(max_length=100)
    kin_age = models.CharField(max_length=10)

    # Documents
    document_type = models.CharField(max_length=100)
    document_front = models.ImageField(upload_to="kyc/")
    document_back = models.ImageField(upload_to="kyc/")

    # Status
    is_approved = models.BooleanField(default=False)
    status = models.CharField(default="processing", max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"KYC - {self.user.email}"
