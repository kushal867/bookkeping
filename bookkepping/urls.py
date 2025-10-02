from django.urls import path
from . import views 

app_name = "bookkeeping"

urlpatterns = [
    path("", views.accounts_list, name="accounts_list"),
    path("transactions/", views.transaction_list, name="transaction_list"),
    path("transactions/new/", views.new_transaction, name="transaction_new"),
    path("reports/trial-balance/", views.trial_balance, name="trial_balance"),
    path("export/ledger.xlsx", views.export_ledger_xlsx, name="export_ledger_xlsx"),
    path("export/trial.pdf", views.export_trial_pdf, name="export_trial_pdf"),
]
