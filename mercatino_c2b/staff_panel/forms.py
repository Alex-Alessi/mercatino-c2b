from django import forms
from proposals.models import ItemProposal

class AdminOfferForm(forms.ModelForm):
    admin_offer = forms.DecimalField(min_value=0, max_digits=8, decimal_places=2, label="Offerta admin",)

    class Meta:
        model = ItemProposal
        fields = ["admin_offer"]