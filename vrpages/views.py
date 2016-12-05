from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from . import forms
from . import models


# def vrpage_qualify_list(request):
#     vrpages = models.VRPage.objects.all()
#     return render(request, 'vrpages/vrpage_qualify_list.html', {'vrpages': vrpages})


# def vrpage_polish_list(request):
#     vrpages = models.VRPage.objects.all()
#     return render(request, 'vrpages/vrpage_polish_list.html', {'vrpages': vrpages})


@login_required
def qualify_polish_list(request):
    vrpages = models.VRPage.objects.all()
    return render(request, 'vrpages/qualify_polish_list.html', {'vrpages': vrpages})


@login_required
def assign_rawurls_list(request):
    vrpages = models.VRPage.objects.all()
    return render(request, 'vrpages/assign_rawurl_list.html', {'vrpages': vrpages})


# def rawurl_qualify(request, pk):
#     try:
#         rawurl = models.RawUrl.objects.filter(vrpage_id=pk).filter(checked=False)[0]
#     except IndexError:
#         return HttpResponseRedirect(reverse('vrpages:no_task', args=[pk]))
#     else:
#         form = forms.RawUrlForm(instance=rawurl)
#         if request.method == 'POST':
#             form = forms.RawUrlForm(instance=rawurl, data=request.POST)
#             if form.is_valid():
#                 form.save()
#                 return HttpResponseRedirect(reverse('vrpages:rawurl_qualify', args=[pk]))
#         return render(request, 'vrpages/rawurl_qualify.html', {'form': form, 'rawurl': rawurl})
#
#
# def rawurl_polish(request, pk):
#     try:
#         rawurl = models.RawUrl.objects.filter(
#             vrpage_id=pk).filter(
#             qualified=True).filter(
#             polishurl__email__isnull=True)[0]
#     except IndexError:
#         return HttpResponseRedirect(reverse('vrpages:no_task', args=[pk]))
#     else:
#         form = forms.PolishUrlForm(initial={'polished_url': rawurl.url})
#         if request.method == 'POST':
#             form = forms.PolishUrlForm(request.POST)
#             if form.is_valid():
#                 polishurl = form.save(commit=False)
#                 polishurl.rawurl = rawurl
#                 polishurl.save()
#                 return HttpResponseRedirect(reverse('vrpages:rawurl_polish', args=[pk]))
#         return render(request, 'vrpages/rawurl_polish.html', {'form': form, 'rawurl': rawurl})


@login_required
def no_task(request, pk):
    vrpage = get_object_or_404(models.VRPage, pk=pk)
    return render(request, 'vrpages/no_task.html', {'vrpage': vrpage})


@login_required
def qualify_polish(request, pk):
    try:
        rawurl = models.RawUrl.objects.filter(vrpage_id=pk).filter(
                checked=False).filter(polisher=request.user)[0]
    except IndexError:
        return HttpResponseRedirect(reverse('vrpages:no_task', args=[pk]))
    else:
        assigned_rawurls = len(models.RawUrl.objects.filter(vrpage_id=pk).filter(
            checked=False).filter(polisher=request.user))
        rawurl_edit = models.RawUrl.objects.get(pk=rawurl.pk)
        form = forms.RawUrlForm(instance=rawurl_edit)
        polishform = forms.PolishUrlForm(vrpage_id=pk, initial={'polished_url': rawurl_edit.url})

        if request.method == 'POST':
            form = forms.RawUrlForm(instance=rawurl_edit, data=request.POST)
            polishform = forms.PolishUrlForm(request.POST, vrpage_id=pk)
            if form.is_valid():
                if form.cleaned_data["qualified"]:
                    if polishform.is_valid():
                        form.save()
                        polishurl = polishform.save(commit=False)
                        polishurl.rawurl = rawurl_edit
                        polishurl.save()
                        return HttpResponseRedirect(reverse(
                            'vrpages:qualify_polish', args=[pk]))
                else:
                    form.save()
                    return HttpResponseRedirect(reverse(
                        'vrpages:qualify_polish', args=[pk]))
        return render(request, 'vrpages/qualify_polish.html', {
            'form': form,
            'polishform': polishform,
            'rawurl': rawurl_edit,
            'assigned_rawurls': assigned_rawurls,
            'polisher': request.user
        })


@login_required
def assign_rawurls(request, pk):
    rawurls = models.RawUrl.objects.filter(vrpage_id=pk).filter(
                checked=False).filter(polisher=None)
    if rawurls:
        form = forms.AssignRawUrlForm()
        if request.method == 'POST':
            form = forms.AssignRawUrlForm(request.POST)
            if form.is_valid():
                total = form.cleaned_data.get("number")
                polisher = form.cleaned_data.get("polisher")
                # assigned_rawurls = models.RawUrl.objects.filter(vrpage_id=pk).filter(
                #     checked=False).filter(polisher=None)[:total]
                assigned_rawurls = models.RawUrl.objects.filter(vrpage_id=pk).filter(
                    checked=False).filter(polisher=None).values_list('pk', flat=True)[:total]
                models.RawUrl.objects.filter(id__in=list(assigned_rawurls)).update(polisher=polisher)
                assign_request = form.save(commit=False)
                assign_request.vrpage = rawurls[0].vrpage
                assign_request.save()
                return HttpResponseRedirect(reverse('vrpages:qualify_polish', args=[pk]))
        return render(request, 'vrpages/assign_rawurl.html', {'rawurls': rawurls, 'form': form})
    return render(request, 'vrpages/assign_rawurl.html', {'rawurls': rawurls})
