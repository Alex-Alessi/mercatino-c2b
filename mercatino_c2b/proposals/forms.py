from django import forms
from .models import ItemProposal, ProposalMessage


class ItemProposalForm(forms.ModelForm):
    images = forms.FileField(
        required=False,
        label="Foto dell'oggetto",
    )

    class Meta:
        model = ItemProposal
        fields = ["title", "description", "requested_price"]
        labels = {
            "title": "Titolo",
            "description": "Descrizione",
            "requested_price": "Prezzo richiesto",
        }


class ProposalMessageForm(forms.ModelForm):
    class Meta:
        model = ProposalMessage
        fields = ["body"]
        labels = {
            "body": "Messaggio",
        }
        widgets = {
            "body": forms.Textarea(attrs={"rows": 3}),
        }


class VintedLinkForm(forms.ModelForm):
    class Meta:
        model = ItemProposal
        fields = ["vinted_url"]
        labels = {
            "vinted_url": "Link annuncio Vinted, Ebay, ecc.",
        }