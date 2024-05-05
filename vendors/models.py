import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import EmailValidator

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CaseInsensitiveEmailField(models.EmailField):
    description = "Email (case-insensitive)"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.append(EmailValidator(message='Enter a valid email address.'))

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value is not None:
            return value.lower()
        return value
    
class Vendor(AbstractUser):
    email = CaseInsensitiveEmailField(unique=True)
    name = models.CharField("Name", max_length=50)
    contact_details = models.CharField("contact details", max_length=150, blank=True)
    address = models.CharField("Address", max_length=150, blank=True)
    vendor_id = models.CharField("vendor id", max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.pk:
            self.vendor_id = uuid.uuid4().hex[:10]  # Generate a 10-character unique code
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=10, default='pending')
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.po_number = f"PO-{uuid.uuid4().hex[:8]}" 
        super().save(*args, **kwargs)

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)