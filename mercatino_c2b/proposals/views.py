from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ItemProposalForm, ProposalMessageForm, VintedLinkForm
from .models import ItemProposal, ProposalImage, ProposalMessage
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

@login_required
def dashboard_view(request):
    proposals = ItemProposal.objects.filter(user=request.user).order_by("-created_at")

    return render(
        request,
        "proposals/dashboard.html",
        {
            "proposals": proposals,
        },
    )


@login_required
def proposal_create_view(request):
    if request.method == "POST":
        form = ItemProposalForm(request.POST, request.FILES)

        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.user = request.user
            proposal.save()

            images = request.FILES.getlist("images")
            for image in images:
                ProposalImage.objects.create(
                    proposal=proposal,
                    image=image,
                )
            messages.success(request, "Proposta inviata correttamente.")
            return redirect("proposal_detail", pk=proposal.pk)
    else:
        form = ItemProposalForm()

    return render(
        request,
        "proposals/proposal_form.html",
        {
            "form": form,
        },
    )


@login_required
def proposal_detail_view(request, pk):
    proposal = get_object_or_404(ItemProposal, pk=pk, user=request.user)
        
    message_form = ProposalMessageForm()
    vinted_form = VintedLinkForm(instance=proposal)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "send_message":
            message_form = ProposalMessageForm(request.POST)
            if message_form.is_valid():
                message = message_form.save(commit=False)
                message.proposal = proposal
                message.sender = request.user
                message.save()

                messages.success(request, "Messaggio inviato.")
                return redirect("proposal_detail", pk=proposal.pk)

        elif action == "send_vinted_link":
            if not proposal.can_user_send_vinted_link():
                messages.error(request, "Non puoi ancora inserire il link dell'annuncio.")
                return redirect("proposal_detail", pk=proposal.pk)

            vinted_form = VintedLinkForm(request.POST, instance=proposal)
            if vinted_form.is_valid():
                proposal = vinted_form.save(commit=False)
                proposal.status = ItemProposal.Status.VINTED_LINK_SENT
                proposal.save()

                send_mail(
                    subject="Nuovo link Vinted ricevuto",
                    message=(
                        f"L'utente {proposal.user.username} "
                        f"ha inserito il link Vinted per la proposta "
                        f"'{proposal.title}'.\n\n"
                        f"Link: {proposal.vinted_url}"
                    ),
                    from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
                    recipient_list=["staff@mercatino.it"],
                    fail_silently=False,
                )

                messages.success(request, "Link Vinted inviato correttamente.")
                return redirect("proposal_detail", pk=proposal.pk)
        
        elif action == "accept_offer":
            if proposal.status != ItemProposal.Status.OFFER_SENT:
                messages.error(request, "Non puoi accettare questa offerta.")
                return redirect("proposal_detail", pk=proposal.pk)
            
            if not proposal.admin_offer:
                messages.error(request, "Non c'è nessuna offerta da accettare.")
                return redirect("proposal_detail", pk=proposal.pk)
            
            proposal.status = ItemProposal.Status.OFFER_ACCEPTED
            proposal.save(update_fields=["status"])

            messages.success(request, "Offerta accettata. Ora puoi inserire il link dell'annuncio.")
            return redirect("proposal_detail", pk=proposal.pk)
    else:
        if proposal.status == ItemProposal.Status.OFFER_SENT and proposal.admin_offer and not proposal.offer_seen_by_user:
            proposal.offer_seen_by_user = True
            proposal.save(update_fields=["offer_seen_by_user"])
            
    return render(
        request,
        "proposals/proposal_detail.html",
        {
            "proposal": proposal,
            "message_form": message_form,
            "vinted_form": vinted_form,
        },
    )