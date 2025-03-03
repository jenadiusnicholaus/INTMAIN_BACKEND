from django.contrib import admin
from .models import Menu, MenuMeta


class MenuMetaAdmin(admin.ModelAdmin):
    list_display = ("icon",)


class MenuAdmin(admin.ModelAdmin):
    list_display = ("name", "display_name", "order")
    filter_horizontal = ("meta",)


admin.site.register(MenuMeta, MenuMetaAdmin)
admin.site.register(Menu, MenuAdmin)
