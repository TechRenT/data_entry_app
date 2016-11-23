from django import forms

from . import models

class RawUrlForm(forms.ModelForm):
    class Meta:
        model = models.RawUrl
        fields = [
            'url',
            'checked',
            'qualified'
        ]


class PolishUrlForm(forms.ModelForm):
    class Meta:
        model = models.PolishUrl
        fields = [
            'rawurl',
            'polished_url',
            'email',
            'page_title',
            'contact_name',
            'broken_link'
        ]
        widgets = {'rawurl': forms.HiddenInput()}