from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from . import models


class RawUrlInline(admin.TabularInline):
    model = models.RawUrl


class VRPageAdmin(admin.ModelAdmin):
    inlines = [RawUrlInline,]


class RawUrlResource(resources.ModelResource):

    class Meta:
        model = models.RawUrl
        fields = ('id', 'domain', 'url', 'source', 'batch', 'checked', 'qualified', 'vrpage')

    def skip_row(self, instance, original):
        rawurls = models.RawUrl.objects.filter(vrpage=instance.vrpage)
        for rawurl in rawurls:
            if rawurl.domain == instance.domain:
                return True
        else:
            return False

@admin.register(models.RawUrl)
class RawUrlAdmin(ImportExportModelAdmin):
    resource_class = RawUrlResource


admin.site.register(models.VRPage, VRPageAdmin)
admin.site.register(models.PolishUrl)
