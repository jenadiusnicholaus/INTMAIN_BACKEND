# Generated by Django 5.1.6 on 2025-03-30 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0032_alter_programstack_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programstack',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
