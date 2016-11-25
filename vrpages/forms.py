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
            #  'rawurl',
            'polished_url',
            'email',
            'page_title',
            'contact_name',
            'broken_link'
        ]
        #  widgets = {'rawurl': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(PolishUrlForm, self).__init__(*args, **kwargs)
        self.fields['polished_url'].required = False
        self.fields['email'].required = False
        self.fields['page_title'].required = False


    def clean(self):
        cleaned_data = super(PolishUrlForm, self).clean()
        polished_url = cleaned_data.get("polished_url")
        email = cleaned_data.get("email")
        page_title = cleaned_data.get("page_title")

        if len(polished_url) == 0:
            raise forms.ValidationError("Polish URL should not be blank")
        if not email:
            raise forms.ValidationError("Please enter a valid email")
        if len(page_title) == 0:
            raise forms.ValidationError("Page Title should not be blank")