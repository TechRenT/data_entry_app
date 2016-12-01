from django import forms

from . import models

class RawUrlForm(forms.ModelForm):
    class Meta:
        model = models.RawUrl
        fields = [
            'checked',
            'qualified',
        ]

    def clean(self):
        cleaned_data = super(RawUrlForm, self).clean()
        checked = cleaned_data.get("checked")
        if not checked:
            raise forms.ValidationError("Make sure the checked field is checked.")


class PolishUrlForm(forms.ModelForm):
    class Meta:
        model = models.PolishUrl
        fields = [
            'polished_url',
            'email',
            'page_title',
            'contact_name',
            'broken_link',
            'domain_authority',
        ]

    def __init__(self, *args, **kwargs):
        self.vrpage_id = kwargs.pop("vrpage_id")
        super(PolishUrlForm, self).__init__(*args, **kwargs)
        self.fields['polished_url'].required = False
        self.fields['email'].required = False
        self.fields['page_title'].required = False
        self.fields['domain_authority'].required = False

    def clean(self):
        cleaned_data = super(PolishUrlForm, self).clean()
        polished_url = cleaned_data.get("polished_url")
        email = cleaned_data.get("email")
        page_title = cleaned_data.get("page_title")
        domain_authority = cleaned_data.get("domain_authority")

        unsubscribes = [str(unsubscribe) for unsubscribe in models.Unsubscribe.objects.all()]
        bounces = [str(bounce) for bounce in models.Bounce.objects.all()]
        polished_emails = [polished.email for polished in models.PolishUrl.objects.filter(rawurl__vrpage=self.vrpage_id)]

        if len(polished_url) == 0:
            raise forms.ValidationError("Polish URL should not be blank")
        if not email:
            raise forms.ValidationError("Please enter a valid email")
        elif email in unsubscribes:
            raise forms.ValidationError("Email is in the unsubscribed list")
        elif email in bounces:
            raise forms.ValidationError("Email is in the bounced list")
        elif email in polished_emails:
            raise forms.ValidationError("Email is already in our database for this VR page")
        if len(page_title) == 0:
            raise forms.ValidationError("Page Title should not be blank")
        if not domain_authority or domain_authority <= 15:
            raise forms.ValidationError("DA must be more than 15")


class AssignRawUrlForm(forms.ModelForm):
    class Meta:
        model = models.AssignRawUrl
        fields = [
            'polisher',
            'number'
        ]