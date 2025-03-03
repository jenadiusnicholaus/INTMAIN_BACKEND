from django.db import models


class MenuMeta(models.Model):
    icon = models.CharField(max_length=255)
    color = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Menu Meta"
        verbose_name_plural = "Menu Metas"


class Menu(models.Model):
    name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    order = models.IntegerField(default=0)
    meta = models.ManyToManyField(MenuMeta)

    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menus"
