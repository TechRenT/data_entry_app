from django.shortcuts import get_object_or_404, render

from . import models


def vrpage_list(request):
    vrpages = models.VRPage.objects.all()
    return render(request, 'vrpages/vrpage_list.html', {'vrpages': vrpages})


def vrpage_detail(request, pk):
    vrpage = get_object_or_404(models.VRPage, pk=pk)
    return render(request, 'vrpages/vrpage_detail.html', {'vrpage': vrpage})


def rawurl_detail(request, vrpage_pk, rawurl_pk):
    raw_url = get_object_or_404(models.RawUrl, vrpage_id=vrpage_pk, id=rawurl_pk)
    return render(request, 'vrpages/rawurl_detail.html', {'raw_url': raw_url})
