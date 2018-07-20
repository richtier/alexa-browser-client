from django import forms


class CompaniesHouseOauth2Form(forms.Form):
    MESSAGE_INVALID_CODE = 'Invalid code.'

    code = forms.CharField(max_length=1000)
