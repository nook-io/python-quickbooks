from typing import ClassVar

from quickbooks.mixins import DeleteMixin
from quickbooks.objects.base import (
    LinkedTxnMixin,
    QuickbooksBaseObject,
    QuickbooksManagedObject,
    QuickbooksTransactionEntity,
    Ref,
)
from quickbooks.objects.detailline import DescriptionOnlyLine, DetailLine
from quickbooks.objects.tax import TxnTaxDetail


class Entity(QuickbooksBaseObject):
    class_dict: ClassVar[dict[str, type]] = {"EntityRef": Ref}

    def __init__(self):
        super().__init__()
        self.Type = ""
        self.EntityRef = None


class JournalEntryLineDetail(QuickbooksBaseObject):
    class_dict: ClassVar[dict[str, type]] = {
        "Entity": Entity,
        "AccountRef": Ref,
        "ClassRef": Ref,
        "DepartmentRef": Ref,
        "TaxCodeRef": Ref,
    }

    def __init__(self):
        super().__init__()
        self.PostingType = ""
        self.TaxApplicableOn = "Sales"
        self.TaxAmount = 0

        self.BillableStatus = None
        self.Entity = None
        self.AccountRef = None
        self.ClassRef = None
        self.DepartmentRef = None
        self.TaxCodeRef = None


class JournalEntryLine(DetailLine):
    class_dict: ClassVar[dict[str, type]] = {"JournalEntryLineDetail": JournalEntryLineDetail}

    def __init__(self):
        super().__init__()
        self.DetailType = "JournalEntryLineDetail"
        self.JournalEntryLineDetail = None


class JournalEntry(DeleteMixin, QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin):
    """
    QBO definition: Journal Entry is a transaction in which:
        - There are at least two parts - a Debit and a Credit - called distribution lines.
        - Each distribution line has an account from the Chart of Accounts.
        - The total of the Debit column equals the total of the Credit column.

        When you record a transaction with Journal Entry, the QBO UI labels the transaction as JRNL in a
        register and General Journal on reports that list transactions.
    """

    class_dict: ClassVar[dict[str, type]] = {"TxnTaxDetail": TxnTaxDetail, "CurrencyRef": Ref}

    list_dict: ClassVar[dict[str, type]] = {"Line": DetailLine}

    detail_dict: ClassVar[dict[str, type]] = {
        "DescriptionOnly": DescriptionOnlyLine,
        "JournalEntryLineDetail": JournalEntryLine,
    }

    qbo_object_name = "JournalEntry"

    def __init__(self):
        super().__init__()
        self.Adjustment = False
        self.TxnDate = ""
        # self.TxnSource = ""
        self.DocNumber = ""
        self.PrivateNote = ""
        self.TotalAmt = 0
        self.ExchangeRate = 1
        self.Line = []
        self.TxnTaxDetail = None

        self.CurrencyRef = None

    def __str__(self):
        return str(self.TotalAmt)
