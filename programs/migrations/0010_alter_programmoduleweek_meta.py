# Generated by Django 5.1.6 on 2025-03-01 19:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu_manager', '0002_rename_title_menumeta_color_remove_menumeta_order'),
        ('programs', '0009_programmodule_display_name_programmodule_meta_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programmoduleweek',
            name='meta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='menu_manager.menumeta'),
        ),
    ]
