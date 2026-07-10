from .models import ItemProposal

def unread_messages(request):
    if not request.user.is_authenticated:
        return {"unread_messages_count": 0}
    
    if request.user.is_staff:
        count = 0

        proposals= ItemProposal.objects.all()

        for proposal in proposals:
            count += proposal.messages.filter(
                sender=proposal.user,
                seen_by_staff=False,
            ).count()
    
    else:
        count = 0

        proposals = ItemProposal.objects.filter(user=request.user)

        for proposal in proposals:
            count += proposal.messages.exclude(
                sender=request.user,
            ).filter(
                seen_by_user=False,
            ).count()

    return {
        "unread_messages_count": count,
    }