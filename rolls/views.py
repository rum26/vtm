from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from .models import Roll
from .forms import RollHistoryForm


@login_required
def roll_list(request):
    rolls = Roll.objects.all().order_by("number")

    return render(
        request,
        "roll_list.html",
        {
            "rolls": rolls
        }
    )


@login_required
def roll_detail(request, roll_id):
    roll = get_object_or_404(Roll, pk=roll_id)

    history = roll.history.all()

    return render(
        request,
        "roll_detail.html",
        {
            "roll": roll,
            "history": history,
        }
    )


@login_required
def add_history(request, roll_id):
    roll = get_object_or_404(Roll, pk=roll_id)

    if request.method == "POST":

        form = RollHistoryForm(request.POST)

        if form.is_valid():

            history = form.save(commit=False)
            history.roll = roll
            history.old_diameter = roll.current_diameter
            history.employee = f"{request.user.last_name} " \
                               f"{request.user.first_name[:1]}."
            history.save()

            return redirect(
                "roll_detail",
                roll_id=roll.id
            )

    else:
        form = RollHistoryForm(
            initial={
                "new_diameter": roll.current_diameter
            }
        )

    return render(
        request,
        "add_history.html",
        {
            "roll": roll,
            "form": form,
        }
    )
