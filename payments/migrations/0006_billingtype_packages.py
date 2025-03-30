# Generated by Django 5.1.6 on 2025-03-30 13:07

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_paymentdisbursementsetting_disbursement_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BillingType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('dicount_percentage', models.IntegerField(default=0)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Packages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(choices=[('Basic', 'Basic'), ('Premium', 'Premium'), ('Enterprise', 'Enterprise'), ('Team', 'Team')], max_length=255)),
                ('description', models.TextField()),
                ('price_per_month', models.DecimalField(decimal_places=2, max_digits=10)),
                ('duration', models.IntegerField(default=0)),
                ('currency', models.CharField(choices=[('USD', 'USD'), ('TZS', 'TZS')], default='TZS', max_length=3)),
                ('is_active', models.BooleanField(default=True)),
                ('discount', models.IntegerField(default=0)),
                ('billing_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.billingtype')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
