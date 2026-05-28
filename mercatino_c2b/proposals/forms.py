from django import forms
from .models import ItemProposal, ProposalMessage

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean

        if isinstance(data, (list, tuple)):
            result = [single_file_clean(file, initial) for file in data]
        else:
            result = single_file_clean(data, initial)

        return result

class ItemProposalForm(forms.ModelForm):
    images = MultipleFileField(
        required=False,
        label="Foto dell'oggetto",
        help_text="Puoi caricare più foto. Da computer selezionale insieme tenendo premuto CTRL o SHIFT"
    )

    class Meta:
        model = ItemProposal
        fields = ["title", "description", "requested_price"]
        labels = {
            "title": "Titolo",
            "description": "Descrizione",
            "requested_price": "Prezzo richiesto",
        }
    
    def clean_images(self):
        images = self.cleaned_data.get("images")

        if not images:
            raise forms.ValidationError("Carica almeno una foto dell'oggetto.")
        
        return images

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