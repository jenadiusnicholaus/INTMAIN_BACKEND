from django.db import models


class Partner(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="partner_logos")

    def __str__(self):
        return self.name
