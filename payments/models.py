from django.db import models
from django.contrib.auth.models import User

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

from utils.bases_models import BaseModel, BaseSoftDeleteModel


class PaymentMethod(BaseModel, BaseSoftDeleteModel):
    """
    PaymentMethod model
    """

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Payment(BaseModel, BaseSoftDeleteModel):
    """
    Payment model
    """

    STATUS_CHOICES = (
        ("paid", "Paid"),
        ("pending", "Pending"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="payments_set"
    )
    transaction_id = models.CharField(max_length=200, null=True, blank=True)
    payment_method = models.ForeignKey(
        PaymentMethod, on_delete=models.CASCADE, related_name="payment_method_set"
    )
    status = models.CharField(
        max_length=200, null=True, blank=True, choices=STATUS_CHOICES
    )
    message = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.date}"

    class Meta:
        verbose_name_plural = "Payments"


class BillingInfo(BaseModel, BaseSoftDeleteModel):
    """
    BillingInfo model
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="billing_info_set",
    )
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    device = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.name}"


class Refund(BaseModel, BaseSoftDeleteModel):
    """
    Refund model
    """

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="refunds_set")
    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, related_name="refund_set"
    )
    transaction_id = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(
        max_length=200, null=True, blank=True, choices=STATUS_CHOICES
    )
    message = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.date}"


class PaymentLog(BaseModel, BaseSoftDeleteModel):
    """
    PaymentLog model
    """

    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, related_name="payment_log_set"
    )
    message = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payment.user.username} - {self.message} - {self.date}"


class RefundLog(BaseModel, BaseSoftDeleteModel):
    """
    RefundLog model
    """

    refund = models.ForeignKey(
        Refund, on_delete=models.CASCADE, related_name="refund_log_set"
    )
    message = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.refund.user.username} - {self.message} - {self.date}"


class PaymentSetting(BaseModel, BaseSoftDeleteModel):
    """
    PaymentSetting model"""

    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class PaymentDisbursement(BaseModel, BaseSoftDeleteModel):
    """ "
    PaymentDisbursement model"
    """

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    Payment_method = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(
        max_length=200, null=True, blank=True, choices=STATUS_CHOICES
    )
    message = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.date}"


class PaymentDisbursementLog(BaseModel, BaseSoftDeleteModel):
    """
    PaymentDisbursementLog model
    """

    payment_disbursement = models.ForeignKey(
        PaymentDisbursement,
        on_delete=models.CASCADE,
        related_name="payment_disbursement_log_set",
    )
    message = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.payment_disbursement.user.username} - {self.message} - {self.date}"
        )


class PaymentDisbursementSetting(BaseModel, BaseSoftDeleteModel):
    """
    PaymentDisbursementSetting model
    """

    disbursement = models.ForeignKey(
        PaymentDisbursement,
        on_delete=models.CASCADE,
        related_name="payment_disbursement_setting_set",
        null=True,
    )
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class BillingType(BaseModel):
    BILLING_TYPE = (
        ("MONTHLY", "Monthly"),
        ("ANNUAL", "Annual"),
        ("ONE_TIME", "One Time"),
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    dicount_percentage = models.IntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Packages(BaseModel):
    NAME_CHOICES = (
        ("Basic", "Basic"),
        ("Premium", "Premium"),
        ("Enterprise", "Enterprise"),
        ("Team", "Team"),
    )

    CURRENCY = (
        ("USD", "USD"),
        ("TZS", "TZS"),
    )

    name = models.CharField(max_length=255, choices=NAME_CHOICES)
    description = models.TextField()
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(default=0)
    currency = models.CharField(max_length=3, choices=CURRENCY, default="TZS")
    is_active = models.BooleanField(default=True)
    billing_type = models.ForeignKey(BillingType, on_delete=models.CASCADE)
    discount = models.IntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
