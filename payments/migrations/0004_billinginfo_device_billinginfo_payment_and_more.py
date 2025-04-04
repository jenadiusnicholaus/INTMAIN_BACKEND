# Generated by Django 5.1.6 on 2025-03-30 11:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_billinginfo_created_at_billinginfo_created_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='billinginfo',
            name='device',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='billinginfo',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='payments.payment'),
        ),
        migrations.AddField(
            model_name='billinginfo',
            name='restored_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='billinginfo',
            name='transaction_id',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='restored_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='paymentdisbursement',
            name='restored_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='paymentdisbursementlog',
            name='restored_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='paymentdisbursementlog',
            name='transaction_id',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='paymentdisbursementsetting',
            name='restored_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='paymentdisbursementsetting',
            name='transaction_id',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='paymentlog',
            name='restored_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='paymentlog',
            name='transaction_id',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='paymentmethod',
            name='restored_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='paymentmethod',
            name='transaction_id',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='paymentsetting',
            name='restored_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='paymentsetting',
            name='transaction_id',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='refund',
            name='restored_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='refundlog',
            name='restored_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='refundlog',
            name='transaction_id',
            field=models.UUIDField(blank=True, null=True),
        ),
    ]
