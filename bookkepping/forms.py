from django import forms
from django.forms import inlineformset_factory
from .models import Transaction, LedgerEntry

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['description']  # 'date' is auto-managed and excluded
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = True

EntryFormSet = inlineformset_factory(
    Transaction, LedgerEntry,
    fields=['account', 'debit', 'credit'],
    extra=2,
    can_delete=False,
    min_num=1,
    validate_min=True
)