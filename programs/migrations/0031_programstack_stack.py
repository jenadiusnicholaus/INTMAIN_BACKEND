# Generated by Django 5.1.6 on 2025-03-30 16:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_stack'),
        ('programs', '0030_rename_is_free_programmoduleweeklesson_to_be_paid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='programstack',
            name='stack',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='program_stacks', to='common.stack'),
        ),
    ]
