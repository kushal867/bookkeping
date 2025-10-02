import io
from django.http import HttpResponse
from openpyxl import Workbook
from .models import LedgerEntry, Account
from xhtml2pdf import pisa
from django.template.loader import render_to_string


def export_ledger_excel():
    wb = Workbook()
    ws = wb.active
    ws.title = 'Ledger'

    # Header row
    ws.append(['Date', 'Transaction', 'Account', 'Debit', 'Credit'])

    # Data rows
    for le in LedgerEntry.objects.select_related('transaction', 'account').order_by('transaction__date'):
        ws.append([
            le.transaction.date.isoformat(),
            le.transaction.description,
            le.account.name,
            float(le.debit),
            float(le.credit)
        ])

    # Save to stream
    stream = io.BytesIO()
    wb.save(stream)
    stream.seek(0)

    response = HttpResponse(
        stream.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=ledger.xlsx'
    return response


def export_trial_balance_pdf():
    accounts = Account.objects.all()

    html = render_to_string('bookkeeping/trial_balance_pdf.html', {
        'accounts': accounts
    })

    result = io.BytesIO()
    pisa.CreatePDF(src=html, dest=result)
    result.seek(0)

    return HttpResponse(result.getvalue(), content_type='application/pdf')
