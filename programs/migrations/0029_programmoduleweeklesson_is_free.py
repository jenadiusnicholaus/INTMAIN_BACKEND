# Generated by Django 5.1.6 on 2025-03-30 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0028_remove_userlearninglessonstatus_pr_review_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='programmoduleweeklesson',
            name='is_free',
            field=models.BooleanField(default=False),
        ),
    ]
