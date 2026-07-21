from django.contrib import admin
from .models import ItemProposal, ProposalImage, ProposalMessage, ProposalEvent

# Register your models here.

class ProposalImageInline(admin.TabularInline):
    model = ProposalImage
    extra = 0
    readonly_fields = ["image"]
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


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
        "mark_as_rejected",
        "mark_as_completed",
    ]
    readonly_fields = [
        "user",
        "title",
        "description",
        "requested_price",
        "vinted_url",
        "status",
        "created_at",
        "updated_at",
    ]

    @admin.action(description="Metti in trattativa")
    def mark_as_negotiation(self, request, queryset):
        queryset.update(status=ItemProposal.Status.NEGOTIATION)

    @admin.action(description="Rifiuta")
    def mark_as_rejected(self, request, queryset):
        queryset.update(status=ItemProposal.Status.REJECTED)

    @admin.action(description="Segna completato")
    def mark_as_completed(self, request, queryset):
        queryset.update(status=ItemProposal.Status.COMPLETED)

    def save_model(self, request, obj, form, change):
        if change:
            old_obj = ItemProposal.objects.get(pk=obj.pk)
            offer_changed = old_obj.admin_offer != obj.admin_offer
        else:
            offer_changed = bool(obj.admin_offer)
        
        if offer_changed and obj.admin_offer:
            if obj.status not in [
                ItemProposal.Status.COMPLETED,
                ItemProposal.Status.VINTED_LINK_SENT,
                ItemProposal.Status.OFFER_ACCEPTED,
            ]:
                obj.status = ItemProposal.Status.OFFER_SENT
                obj.offer_seen_by_user = False
        super().save_model(request, obj, form, change)
    
    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))

        if obj and obj.status in [
            ItemProposal.Status.OFFER_ACCEPTED,
            ItemProposal.Status.VINTED_LINK_SENT,
            ItemProposal.Status.COMPLETED,
        ]:
            readonly.append("admin_offer")
        
        return readonly


@admin.register(ProposalImage)
class ProposalImageAdmin(admin.ModelAdmin):
    list_display = ["proposal", "image"]


@admin.register(ProposalMessage)
class ProposalMessageAdmin(admin.ModelAdmin):
    list_display = ["proposal", "sender", "created_at"]
    search_fields = ["body", "sender__username", "proposal__title"]

@admin.register(ProposalEvent)
class ProposalEventAdmin(admin.ModelAdmin):
    list_display = (
        "proposal",
        "event_type",
        "created_at",
    )

    list_filter = (
        "event_type",
        "created_at",
    )

    search_fields = (
        "proposal__title",
        "proposal__user__username",
    )

    ordering = ("-created_at",)