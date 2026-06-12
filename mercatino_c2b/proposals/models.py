from django.db import models
from django.conf import settings

# Create your models here.

class ItemProposal(models.Model):
    class Status(models.TextChoices):
        UNDER_REVIEW = "under_review", "In valutazione"
        NEGOTIATION = "negotiation", "In trattativa"
        OFFER_SENT = "offer_sent", "Offerta inviata"
        OFFER_ACCEPTED = "offer_accepted", "Offerta accettata"
        WAITING_VINTED_LINK = "waiting_vinted_link", "In attesa link Vinted"
        VINTED_LINK_SENT = "vinted_link_sent", "Link Vinted inviato"
        COMPLETED = "completed", "Completato"
        REJECTED = "rejected", "Rifiutato"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="proposals",
    )
    title = models.CharField(max_length=120)
    description = models.TextField()
    requested_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )
    admin_offer = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.UNDER_REVIEW,
    )
    vinted_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    offer_seen_by_user = models.BooleanField(default=False)

    def can_user_send_vinted_link(self):
        return self.status in [
            self.Status.OFFER_ACCEPTED,
            self.Status.WAITING_VINTED_LINK,
        ]
    
    @property
    def status_badge_class(self):
        classes = {
            self.Status.UNDER_REVIEW: "badge-gray",
            self.Status.NEGOTIATION: "badge-blue",
            self.Status.OFFER_SENT: "badge-purple",
            self.Status.OFFER_ACCEPTED: "badge-green",
            self.Status.WAITING_VINTED_LINK: "badge-orange",
            self.Status.VINTED_LINK_SENT: "badge-orange",
            self.Status.COMPLETED: "badge-green",
            self.Status.REJECTED: "badge-red",
        }

        return classes.get(self.status, "badge-gray")

    def can_be_deleted(self):
        return(
            self.status == self.Status.UNDER_REVIEW
            and not self.messages.exists()
            and not self.admin_offer
        )

    def __str__(self):
        return self.title


class ProposalImage(models.Model):
    proposal = models.ForeignKey(
        ItemProposal,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to="proposals/")

    def __str__(self):
        return f"Immagine per {self.proposal.title}"


class ProposalMessage(models.Model):
    proposal = models.ForeignKey(
        ItemProposal,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    body = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Messaggio di {self.sender}"