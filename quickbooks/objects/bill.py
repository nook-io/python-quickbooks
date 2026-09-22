from typing import ClassVar

from quickbooks.mixins import DeleteMixin
from quickbooks.objects.base import LinkedTxn, LinkedTxnMixin, QuickbooksManagedObject, QuickbooksTransactionEntity, Ref
from quickbooks.objects.detailline import AccountBasedExpenseLine, DetailLine, ItemBasedExpenseLine, TDSLine
from quickbooks.objects.tax import TxnTaxDetail


class Bill(DeleteMixin, QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin):
    """
    QBO definition: A Bill entity is an AP transaction representing a request-for-payment from a third party for
    goods/services rendered and/or received.
    """

    class_dict: ClassVar[dict[str, type]] = {
        "SalesTermRef": Ref,
        "CurrencyRef": Ref,
        "APAccountRef": Ref,
        "VendorRef": Ref,
        "AttachableRef": Ref,
        "DepartmentRef": Ref,
        "TxnTaxDetail": TxnTaxDetail,
    }

    list_dict: ClassVar[dict[str, type]] = {"Line": DetailLine, "LinkedTxn": LinkedTxn}

    detail_dict: ClassVar[dict[str, type]] = {
        "ItemBasedExpenseLineDetail": ItemBasedExpenseLine,
        "AccountBasedExpenseLineDetail": AccountBasedExpenseLine,
        "TDSLineDetail": TDSLine,
    }

    qbo_object_name = "Bill"

    def __init__(self):
        super().__init__()

        self.DueDate = ""
        self.Balance = 0
        self.TotalAmt = ""
        self.TxnDate = ""
        self.DocNumber = ""
        self.PrivateNote = ""
        self.ExchangeRate = 0
        self.GlobalTaxCalculation = None

        self.SalesTermRef = None
        self.CurrencyRef = None
        self.AttachableRef = None
        self.VendorRef = None
        self.DepartmentRef = None
        self.APAccountRef = None

        self.LinkedTxn = []
        self.Line = []

    def __str__(self):
        return str(self.Balance)

    def to_linked_txn(self):
        linked_txn = LinkedTxn()
        linked_txn.TxnId = self.Id
        linked_txn.TxnType = "Bill"
        linked_txn.TxnLineId = 1

        return linked_txn

    def to_ref(self):
        ref = Ref()

        ref.name = self.DocNumber
        ref.type = self.qbo_object_name
        ref.value = self.Id

        return ref
