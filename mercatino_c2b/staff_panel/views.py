from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from proposals.models import ItemProposal
from proposals.forms import ProposalMessageForm
from django.contrib import messages
from .forms import AdminOfferForm
from proposals.utils import send_notification_email


# Create your views here.
@login_required
@user_passes_test(lambda user: user.is_staff)
def staff_proposal_list_view(request):
    selected_status = request.GET.get("status")
    
    proposals = ItemProposal.objects.all()

    if selected_status:
        proposals = proposals.filter(status=selected_status)

    proposals = proposals.order_by("-created_at")

    return render(request, "staff_panel/proposal_list.html", {
        "proposals": proposals,
        "selected_status": selected_status,
        "status_choices": ItemProposal.Status.choices,
    })

@login_required
@user_passes_test(lambda user: user.is_staff)
def staff_proposal_detail_view(request, pk):
    proposal = get_object_or_404(ItemProposal, pk=pk)
    message_form = ProposalMessageForm()
    offer_form = AdminOfferForm(instance=proposal)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "send_message":
            message_form = ProposalMessageForm(request.POST)

            if message_form.is_valid():
                message = message_form.save(commit=False)
                message.proposal = proposal
                message.sender = request.user
                message.save()

                if proposal.user.email:
                    send_notification_email(
                        subject="Hai ricevuto un nuovo messaggio",
                        message=(
                            f"Ciao {proposal.user.first_name or proposal.user.username},\n\n"
                            f"Hai ricevuto un nuovo messaggio riguardo alla proposta "
                            f"'{proposal.title}'.\n\n"
                            f"Accedi al sito per leggerlo e rispondere."
                        ),
                        recipients=[proposal.user.email],
                    )

                messages.success(request, "Messaggio inviato.")
                return redirect("staff_proposal_detail", pk=proposal.pk)
            
        elif action == "send_offer":
            offer_form = AdminOfferForm(request.POST, instance=proposal)

            if offer_form.is_valid():
                proposal = offer_form.save(commit=False)
                proposal.status = ItemProposal.Status.OFFER_SENT
                proposal.offer_seen_by_user = False
                proposal.save(update_fields=["admin_offer", "status", "offer_seen_by_user", "updated_at"])

                if proposal.user.email:
                    send_notification_email(
                        subject="Hai ricevuto una nuova offerta",
                        message=(
                            f"Ciao {proposal.user.first_name or proposal.user.username},\n\n"
                            f"Abbiamo valutato la tua proposta '{proposal.title}'.\n\n"
                            f"La nostra offerta è di € {proposal.admin_offer}.\n\n"
                            f"Accedi al sito per visualizzare i dettagli e continuare la trattativa."
                        ),
                        recipients=[proposal.user.email],
                    )

                messages.success(request, "Offerta inviata correttamente.")
                return redirect("staff_proposal_detail", pk=proposal.pk)
        
        elif action == "mark_negotiation":
            proposal.status = ItemProposal.Status.NEGOTIATION
            proposal.save(update_fields=["status"])

            messages.success(request, "Proposta messa in trattativa.")
            return redirect("staff_proposal_detail", pk=proposal.pk)
        
        elif action == "reject":
            proposal.status = ItemProposal.Status.REJECTED
            proposal.save(update_fields=["status"])

            if proposal.user.email:
                send_notification_email(
                    subject="Aggiornamento sulla tua proposta",
                    message=(
                        f"Ciao {proposal.user.first_name or proposal.user.username},\n\n"
                        f"Dopo la valutazione, la proposta '{proposal.title}' "
                        f"non è stata accettata.\n\n"
                        f"Ti ringraziamo per aver utilizzato il nostro servizio."
                    ),
                    recipients=[proposal.user.email],
                )

            messages.success(request, "Proposta rifiutata.")
            return redirect("staff_proposal_detail", pk=proposal.pk)

        elif action == "complete":
            proposal.status = ItemProposal.Status.COMPLETED
            proposal.save(update_fields=["status"])

            messages.success(request, "Proposta completata.")
            return redirect("staff_proposal_detail", pk=proposal.pk)

    return render(request, "staff_panel/proposal_detail.html", {
    "proposal": proposal,
    "message_form": message_form,
    "offer_form": offer_form,
    })

