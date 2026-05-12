from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from proposals.models import ItemProposal
from proposals.forms import ProposalMessageForm
from django.contrib import messages
from .forms import AdminOfferForm

# Create your views here.
@login_required
@user_passes_test(lambda user: user.is_staff)
def staff_proposal_list_view(request):
    proposals = ItemProposal.objects.all().order_by("-created_at")

    return render(request, "staff_panel/proposal_list.html", {
        "proposals": proposals,
    },)

@login_required
@user_passes_test(lambda user: user.is_staff)
def staff_proposal_detail_view(request, pk):
    proposal = get_object_or_404(ItemProposal, pk=pk)
    message_form = ProposalMessageForm()
    offer_form = AdminOfferForm()

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
                return redirect("staff_proposal_detail", pk=proposal.pk)

    return render(request, "staff_panel/proposal_detail.html", {
    "proposal": proposal,
    "message_form": message_form,
    "offer_form": offer_form,
    })

