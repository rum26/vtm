from django import forms
from .models import RollHistory


class RollHistoryForm(forms.ModelForm):
    class Meta:
        model = RollHistory

        fields = [
            "status",
            "new_diameter",
            "comment",
        ]
