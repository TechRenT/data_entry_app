from django.contrib import admin

from . import models


class RawUrlInline(admin.StackedInline):
    model = models.RawUrl


class VRPageAdmin(admin.ModelAdmin):
    inlines = [RawUrlInline,]

admin.site.register(models.VRPage, VRPageAdmin)
admin.site.register(models.RawUrl)

