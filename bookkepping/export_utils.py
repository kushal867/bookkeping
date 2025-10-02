import io
from django.http import HttpResponse
from openpyxl import Workbook
from .models import LedgerEntry, Account
from xhtml2pdf import pisa
from django.template.loader import render_to_string

# Export ledger to Excel

def export_ledger_excel():
    wb = Workbook()
    ws = wb.active
    ws.title = 'Ledger'
    ws.append(['Date', 'Transaction', 'Account', 'Debit', 'Credit'])
    for le in LedgerEntry.objects.select_related('transaction', 'account').order_by('transaction__date'):
        ws.append([le.transaction.date.isoformat(), le.transaction.description, le.account.name, float(le.debit), float(le.credit)])
    stream = io.BytesIO()
    wb.save(stream)
    stream.seek(0)
    response = HttpResponse(stream.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=ledger.xlsx'
    return response

# Export trial balance to PDF

def export_trial_balance_pdf():
    from django.db.models import Sum
    accounts = Account.objects.all().annotate(
        debit_total=Sum('ledgerentry__debit'),
        credit_total=Sum('ledgerentry__credit')
    )
    
    # Calculate totals and difference
    total_debits = sum((a.debit_total or 0) for a in accounts)
    total_credits = sum((a.credit_total or 0) for a in accounts)
    difference = total_debits - total_credits
    
    context = {
        'accounts': accounts,
        'total_debits': total_debits,
        'total_credits': total_credits,
        'difference': difference,
    }
    
    html = render_to_string('bookkepping/trial_balance_pdf.html', context)
    result = io.BytesIO()
    pisa.CreatePDF(src=html, dest=result)
    result.seek(0)
    return HttpResponse(result.getvalue(), content_type='application/pdf')