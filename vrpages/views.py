from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from . import forms
from . import models


def vrpage_qualify_list(request):
    vrpages = models.VRPage.objects.all()
    return render(request, 'vrpages/vrpage_qualify_list.html', {'vrpages': vrpages})


def vrpage_polish_list(request):
    vrpages = models.VRPage.objects.all()
    return render(request, 'vrpages/vrpage_polish_list.html', {'vrpages': vrpages})


def rawurl_qualify(request, pk):
    try:
        rawurl = models.RawUrl.objects.filter(vrpage_id=pk).filter(checked=False)[0]
    except IndexError:
        return HttpResponseRedirect(reverse('vrpages:qualify_list'))
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
        rawurl = models.RawUrl.objects.filter(
            vrpage_id=pk).filter(
            qualified=True).filter(
            polishurl__email__isnull=True)[0]
    except IndexError:
        return HttpResponseRedirect(reverse('vrpages:polish_list'))
    else:
        form = forms.PolishUrlForm(initial={'polished_url': rawurl.url, 'rawurl': rawurl.pk})
        if request.method == 'POST':
            form = forms.PolishUrlForm(request.POST)
            if form.is_valid():
                form.save()
            return HttpResponseRedirect(reverse('homepage'))
        return render(request, 'vrpages/rawurl_polish.html', {'form': form, 'rawurl': rawurl})