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
        fields = (
            'id',
            'domain',
            'url',
            'source',
            'batch',
            'checked',
            'qualified',
            'vrpage'
        )

    def skip_row(self, instance, original):
        rawurls = models.RawUrl.objects.filter(vrpage=instance.vrpage)
        for rawurl in rawurls:
            if rawurl.url == instance.url:
                return True
        polished_urls = models.PolishUrl.objects.filter(rawurl_id__vrpage_id=instance.vrpage)
        for url in polished_urls:
            if instance.domain == url.rawurl.domain:
                return True
        else:
            return False


class UnsubscribeResource(resources.ModelResource):

    class Meta:
        model = models.Unsubscribe
        fields = ('id', 'email', 'vrpage')


class BounceResource(resources.ModelResource):

    class Meta:
        model = models.Bounce
        fields = ('id', 'email', 'vrpage')


class PolishUrlResource(resources.ModelResource):

    class Meta:
        model = models.PolishUrl
        fields = (
            'id',
            'created_at',
            'rawurl',
            'polished_url',
            'email',
            'page_title',
            'contact_name',
            'broken_link',
            'domain_authority',
        )


@admin.register(models.RawUrl)
class RawUrlAdmin(ImportExportModelAdmin):
    resource_class = RawUrlResource


@admin.register(models.Unsubscribe)
class UnsubscribeAdmin(ImportExportModelAdmin):
    resource_class = UnsubscribeResource


@admin.register(models.Bounce)
class BounceAdmin(ImportExportModelAdmin):
    resource_class = BounceResource


@admin.register(models.PolishUrl)
class PolishUrlAdmin(ImportExportModelAdmin):
    resource_class = PolishUrlResource


admin.site.register(models.VRPage, VRPageAdmin)
admin.site.register(models.AssignRawUrl)
