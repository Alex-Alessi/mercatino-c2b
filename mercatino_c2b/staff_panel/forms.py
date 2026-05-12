from django import forms

class AdminOfferForm(forms.ModelForm):
    admin_offer = forms.PositiveIntegerField()