from decimal import Decimal

from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404

from .models import Account, Transaction
from .forms import TransactionForm, EntryFormSet
from .export_utils import export_ledger_excel, export_trial_balance_pdf


def accounts_list(request):
    accounts = Account.objects.order_by('type', 'name')
    return render(request, 'bookkepping/accounts_list.html', {'accounts': accounts})


def new_transaction(request):
    if request.method == 'POST':
        tform = TransactionForm(request.POST)
        eformset = EntryFormSet(request.POST)

        if tform.is_valid() and eformset.is_valid():
            tx = tform.save(commit=False)
            entries = []

            for ef in eformset:
                if ef.cleaned_data:  # avoid errors for empty forms
                    acct = ef.cleaned_data.get('account')
                    debit = ef.cleaned_data.get('debit') or Decimal('0')
                    credit = ef.cleaned_data.get('credit') or Decimal('0')

                    if acct and (debit or credit):
                        entries.append({
                            'account': acct.pk,
                            'debit': debit,
                            'credit': credit
                        })

            try:
                tx.save_with_entries(entries)
            except Exception as e:
                tform.add_error(None, str(e))
            else:
                return redirect('bookkeeping:transaction_list')
    else:
        tform = TransactionForm()
        eformset = EntryFormSet()

    return render(request, 'bookkepping/transaction_form.html', {
        'tform': tform,
        'eformset': eformset
    })


def transaction_list(request):
    txs = Transaction.objects.prefetch_related('entries__account').order_by('-date')
    return render(request, 'bookkepping/transaction_list.html', {'transactions': txs})


def trial_balance(request):
    accounts = Account.objects.all().annotate(
        debit_total=Sum('ledgerentry__debit'),
        credit_total=Sum('ledgerentry__credit')
    )

    # compute totals
    total_debits = sum((a.debit_total or 0) for a in accounts)
    total_credits = sum((a.credit_total or 0) for a in accounts)

    # Calculate difference
    difference = total_debits - total_credits
    
    return render(request, 'bookkepping/trial_balance.html', {
        'accounts': accounts,
        'total_debits': total_debits,
        'total_credits': total_credits,
        'difference': difference,
    })




def export_ledger_xlsx(request):
    return export_ledger_excel()


def export_trial_pdf(request):
    return export_trial_balance_pdf()
