# Generated by Django 5.1.6 on 2025-03-11 11:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0017_programstacks'),
    ]

    operations = [
        migrations.AddField(
            model_name='programstacks',
            name='program',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='programs.program'),
        ),
    ]
