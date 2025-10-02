from django import forms
from django.forms import formset_factory
from .models import Transaction, Account


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('date', 'description')


class EntryForm(forms.Form):
    account = forms.ModelChoiceField(queryset=Account.objects.all())
    debit = forms.DecimalField(max_digits=14, decimal_places=2, required=False, initial=0)
    credit = forms.DecimalField(max_digits=14, decimal_places=2, required=False, initial=0)


EntryFormSet = formset_factory(EntryForm, extra=2)
