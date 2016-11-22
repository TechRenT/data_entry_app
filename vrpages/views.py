from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from . import forms
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


def rawurl_qualify(request, pk):
    try:
        rawurl = models.RawUrl.objects.filter(vrpage_id=pk).filter(checked=False)[0]
    except IndexError:
        return HttpResponseRedirect(reverse('vrpages:list'))
    else:
        form = forms.RawUrlForm(instance=rawurl)
        if request.method == 'POST':
            form = forms.RawUrlForm(instance=rawurl, data=request.POST)
            if form.is_valid():
                form.save()
            return HttpResponseRedirect(reverse('vrpages:rawurl_qualify', args=[pk]))
        return render(request, 'vrpages/rawurl_qualify.html', {'form': form})


def rawurl_polish(request, pk):
    try:
        rawurl = models.RawUrl.objects.filter(vrpage_id=pk).filter(qualified=True)[0]
    except IndexError:
        return HttpResponseRedirect(reverse('vrpages:list'))
    else:
        form = forms.PolishUrlForm(initial={'polished_url': rawurl.url})
        if request.method == 'POST':
            form = forms.PolishUrlForm(request.POST)
            if form.is_valid():
                form.save()
            return HttpResponseRedirect(reverse('homepage'))
        return render(request, 'vrpages/rawurl_polish.html', {'form': form, 'rawurl': rawurl})