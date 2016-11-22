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