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
