from django.core.urlresolvers import reverse
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render

from . import forms
from . import models


def vrpage_qualify_list(request):
    vrpages = models.VRPage.objects.all()
    return render(request, 'vrpages/vrpage_qualify_list.html', {'vrpages': vrpages})


def vrpage_polish_list(request):
    vrpages = models.VRPage.objects.all()
    return render(request, 'vrpages/vrpage_polish_list.html', {'vrpages': vrpages})


def qualify_polish_list(request):
    vrpages = models.VRPage.objects.all()
    return render(request, 'vrpages/qualify_polish_list.html', {'vrpages': vrpages})


def assign_rawurls_list(request):
    vrpages = models.VRPage.objects.all()
    return render(request, 'vrpages/assign_rawurl_list.html', {'vrpages': vrpages})


def rawurl_qualify(request, pk):
    try:
        rawurl = models.RawUrl.objects.filter(vrpage_id=pk).filter(checked=False)[0]
    except IndexError:
        return HttpResponseRedirect(reverse('vrpages:no_task', args=[pk]))
    else:
        form = forms.RawUrlForm(instance=rawurl)
        if request.method == 'POST':
            form = forms.RawUrlForm(instance=rawurl, data=request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('vrpages:rawurl_qualify', args=[pk]))
        return render(request, 'vrpages/rawurl_qualify.html', {'form': form, 'rawurl': rawurl})


def rawurl_polish(request, pk):
    try:
        rawurl = models.RawUrl.objects.filter(
            vrpage_id=pk).filter(
            qualified=True).filter(
            polishurl__email__isnull=True)[0]
    except IndexError:
        return HttpResponseRedirect(reverse('vrpages:no_task', args=[pk]))
    else:
        form = forms.PolishUrlForm(initial={'polished_url': rawurl.url})
        if request.method == 'POST':
            form = forms.PolishUrlForm(request.POST)
            if form.is_valid():
                polishurl = form.save(commit=False)
                polishurl.rawurl = rawurl
                polishurl.save()
                return HttpResponseRedirect(reverse('vrpages:rawurl_polish', args=[pk]))
        return render(request, 'vrpages/rawurl_polish.html', {'form': form, 'rawurl': rawurl})


def no_task(request, pk):
    vrpage = get_object_or_404(models.VRPage, pk=pk)
    return render(request, 'vrpages/no_task.html', {'vrpage': vrpage})


def qualify_polish(request, pk):
    try:
        rawurl = models.RawUrl.objects.filter(vrpage_id=pk).filter(
                checked=False)[0]
    except IndexError:
        return HttpResponseRedirect(reverse('vrpages:no_task', args=[pk]))
    else:
        form = forms.RawUrlForm(instance=rawurl)
        polishform = forms.PolishUrlForm(initial={'polished_url': rawurl.url})

        if request.method == 'POST':
            updated_rawurl = models.RawUrl.objects.get(id=rawurl.pk)
            updated_rawurl.polisher = request.user
            updated_rawurl.save()
            form = forms.RawUrlForm(instance=updated_rawurl, data=request.POST)
            polishform = forms.PolishUrlForm(request.POST)
            if form.is_valid():
                if form.cleaned_data["qualified"]:
                    if polishform.is_valid():
                        form.save()
                        polishurl = polishform.save(commit=False)
                        polishurl.rawurl = rawurl
                        polishurl.save()
                        return HttpResponseRedirect(reverse
                                ('vrpages:qualify_polish', args=[pk]))
                else:
                    form.save()
                    return HttpResponseRedirect(reverse
                                ('vrpages:qualify_polish', args=[pk]))
        return render(request, 'vrpages/qualify_polish.html', {'form': form,
                                                    'polishform': polishform,
                                                    'rawurl': rawurl,
                                                    'polisher': request.user})


def assign_rawurls(request, pk):
    rawurls = models.RawUrl.objects.filter(vrpage_id=pk).filter(
                checked=False).filter(polisher=None)
    if rawurls:
        form = forms.AssignRawUrlForm()
        if request.method == 'POST':
            if form.is_valid():
                assign_request = form.save(commit=False)
                assign_request.vrpage = pk
                assign_request.save()
        return render(request, 'vrpages/assign_rawurl.html', {'rawurls': rawurls, 'form': form})
    return render(request, 'vrpages/assign_rawurl.html', {'rawurls': rawurls})
