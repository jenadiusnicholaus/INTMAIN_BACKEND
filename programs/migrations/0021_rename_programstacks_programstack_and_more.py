# Generated by Django 5.1.6 on 2025-03-11 13:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0020_programmoreinfo'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProgramStacks',
            new_name='ProgramStack',
        ),
        migrations.AlterField(
            model_name='programmoreinfo',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='more_info_set', to='programs.program'),
        ),
    ]
