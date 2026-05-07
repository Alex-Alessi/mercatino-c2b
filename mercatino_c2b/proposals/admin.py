from django.contrib import admin
from .models import ItemProposal, ProposalImage, ProposalMessage

# Register your models here.

class ProposalImageInline(admin.TabularInline):
    model = ProposalImage
    extra = 0


class ProposalMessageInline(admin.TabularInline):
    model = ProposalMessage
    extra = 0
    readonly_fields = ["created_at"]


@admin.register(ItemProposal)
class ItemProposalAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "user",
        "status",
        "requested_price",
        "admin_offer",
        "created_at",
    ]
    list_filter = ["status", "created_at"]
    search_fields = ["title", "description", "user__username", "user__email"]
    inlines = [ProposalImageInline, ProposalMessageInline]
    actions = [
        "mark_as_negotiation",
        "mark_as_offer_accepted",
        "mark_as_rejected",
        "mark_as_completed",
    ]
    readonly_fields = [
        "user",
        "title",
        "description",
        "requested_price",
        "vinted_url",
        "created_at",
        "updated_at",
    ]

    @admin.action(description="Metti in trattativa")
    def mark_as_negotiation(self, request, queryset):
        queryset.update(status=ItemProposal.Status.NEGOTIATION)

    @admin.action(description="Segna offerta accettata")
    def mark_as_offer_accepted(self, request, queryset):
        queryset.update(status=ItemProposal.Status.OFFER_ACCEPTED)

    @admin.action(description="Rifiuta")
    def mark_as_rejected(self, request, queryset):
        queryset.update(status=ItemProposal.Status.REJECTED)

    @admin.action(description="Segna completato")
    def mark_as_completed(self, request, queryset):
        queryset.update(status=ItemProposal.Status.COMPLETED)


@admin.register(ProposalImage)
class ProposalImageAdmin(admin.ModelAdmin):
    list_display = ["proposal", "image"]


@admin.register(ProposalMessage)
class ProposalMessageAdmin(admin.ModelAdmin):
    list_display = ["proposal", "sender", "created_at"]
    search_fields = ["body", "sender__username", "proposal__title"]