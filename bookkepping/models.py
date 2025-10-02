from decimal import Decimal
from django.db import models, transaction
from django.core.exceptions import ValidationError


class Account(models.Model):
    TYPE_CHOICES = [
        ('asset', 'Asset'),
        ('liability', 'Liability'),
        ('equity', 'Equity'),
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f"{self.name} ({self.type})"


class Transaction(models.Model):
    date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=255)

    def clean(self):
        """Check that debits = credits."""
        if hasattr(self, "_entries_preview"):
            debits = sum(Decimal(ed.get("debit") or 0) for ed in self._entries_preview)
            credits = sum(Decimal(ed.get("credit") or 0) for ed in self._entries_preview)
        else:
            # Only validate if entries exist and transaction has been saved
            if self.pk and hasattr(self, 'entries') and self.entries.exists():
                debits = sum(self.entries.values_list("debit", flat=True))
                credits = sum(self.entries.values_list("credit", flat=True))
            else:
                return  # Skip validation if no entries or not saved yet

        if debits != credits:
            raise ValidationError("Transaction is not balanced: total debits must equal total credits")

    def save_with_entries(self, entries_data):
        """
        Atomic save of transaction and ledger entries.
        entries_data: list of dicts: {'account': Account.pk, 'debit': Decimal, 'credit': Decimal}
        """
        # preview entries for clean()
        self._entries_preview = entries_data
        self.clean()

        with transaction.atomic():
            self.save()
            created_entries = []
            for ed in entries_data:
                acc = Account.objects.select_for_update().get(pk=ed['account'])
                debit = Decimal(ed.get('debit') or 0)
                credit = Decimal(ed.get('credit') or 0)

                if debit and credit:
                    raise ValidationError("An entry cannot have both debit and credit")

                le = LedgerEntry.objects.create(
                    transaction=self,
                    account=acc,
                    debit=debit,
                    credit=credit,
                )

                # update balance depending on account type
                if acc.type in ('asset', 'expense'):
                    acc.balance = acc.balance + debit - credit
                else:
                    acc.balance = acc.balance - debit + credit
                acc.save()

                created_entries.append(le)

            return created_entries

    def __str__(self):
        return f"{self.date} - {self.description}"


class LedgerEntry(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='entries')
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    debit = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    credit = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))

    def clean(self):
        if self.debit and self.credit:
            raise ValidationError("Entry cannot have both debit and credit")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.account.name}: Dr {self.debit} Cr {self.credit}"
