from django.db import models


class VRPage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    client = models.CharField(max_length=255)
    url = models.URLField(max_length=200)

    def __str__(self):
        return self.name

