from typing import ClassVar

from quickbooks.mixins import DeleteMixin
from quickbooks.objects.base import LinkedTxnMixin, QuickbooksManagedObject, QuickbooksTransactionEntity, Ref
from quickbooks.objects.detailline import AccountBasedExpenseLine, DetailLine, ItemBasedExpenseLine, TDSLine


class VendorCredit(DeleteMixin, QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin):
    """
    QBO definition: The Vendor Credit entity is an accounts payable transaction that represents a refund or credit
    of payment for goods or services. It is a credit that a vendor owes you for various reasons such as overpaid
    bill, returned merchandise, or other reasons.
    """

    class_dict: ClassVar[dict[str, type]] = {
        "VendorRef": Ref,
        "APAccountRef": Ref,
        "DepartmentRef": Ref,
        "CurrencyRef": Ref,
    }

    list_dict: ClassVar[dict[str, type]] = {"Line": DetailLine}

    detail_dict: ClassVar[dict[str, type]] = {
        "AccountBasedExpenseLineDetail": AccountBasedExpenseLine,
        "ItemBasedExpenseLineDetail": ItemBasedExpenseLine,
        "TDSLineDetail": TDSLine,
    }

    qbo_object_name = "VendorCredit"

    def __init__(self):
        super().__init__()
        self.DocNumber = ""
        self.TxnDate = ""
        self.PrivateNote = ""
        self.TotalAmt = 0
        self.ExchangeRate = 1
        self.GlobalTaxCalculation = "TaxExcluded"

        self.FromAccountRef = None
        self.ToAccountRef = None

        self.LinkedTxn = []
        self.Line = []

    def __str__(self):
        return str(self.TotalAmt)
