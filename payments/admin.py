from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Payment)
admin.site.register(PaymentMethod)
admin.site.register(BillingInfo)
admin.site.register(Refund)
admin.site.register(PaymentLog)
admin.site.register(RefundLog)
admin.site.register(PaymentSetting)
admin.site.register(PaymentDisbursement)
admin.site.register(PaymentDisbursementLog)
admin.site.register(PaymentDisbursementSetting)
admin.site.register(BillingType)
admin.site.register(Packages)
