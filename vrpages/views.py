from django.http import HttpResponse
from django.shortcuts import render

from . import models

def vrpage_list(request):
    vrpages = models.VRPage.objects.all()
    return render(request, 'vrpages/vrpage_list.html', {'vrpages': vrpages})

