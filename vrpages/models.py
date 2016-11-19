from django.db import models


class VRPage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    client = models.CharField(max_length=255)
    url = models.URLField(max_length=200)

    def __str__(self):
        return self.name


class RawUrl(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField(max_length=200)
    source = models.CharField(max_length=30)
    batch = models.CharField(max_length=30)
    checked = models.BooleanField(default=False)
    qualified = models.BooleanField(default=False)
    vrpage = models.ForeignKey(VRPage)

    def __str__(self):
        return self.url
