from django.contrib.auth.models import User
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
    domain = models.CharField(max_length=30, default='')
    url = models.URLField(max_length=200)
    source = models.CharField(max_length=30)
    batch = models.CharField(max_length=30)
    checked = models.BooleanField(default=False)
    qualified = models.BooleanField(default=False)
    vrpage = models.ForeignKey(VRPage)
    polisher = models.ForeignKey(User, related_name='polishurls', blank=True, null=True)

    def __str__(self):
        return self.url


class PolishUrl(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    rawurl = models.OneToOneField(RawUrl)
    polished_url = models.URLField(max_length=200)
    email = models.EmailField()
    page_title = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=30, blank=True)
    broken_link = models.CharField(max_length=255, blank=True)
    domain_authority = models.IntegerField()

    def __str__(self):
        return self.polished_url


class AssignRawUrl(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    vrpage = models.ForeignKey(VRPage)
    polisher = models.ForeignKey(User)
    number = models.IntegerField()

    def __str__(self):
        return self.polisher.username


class Unsubscribe(models.Model):
    email = models.EmailField()
    vrpage = models.ForeignKey(VRPage, blank=True, null=True)

    def __str__(self):
        return self.email


class Bounce(models.Model):
    email = models.EmailField()
    vrpage = models.ForeignKey(VRPage, blank=True, null=True)

    def __str__(self):
        return self.email