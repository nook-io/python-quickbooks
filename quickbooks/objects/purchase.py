from typing import ClassVar

from quickbooks.mixins import DeleteMixin
from quickbooks.objects.base import (
    Address,
    LinkedTxn,
    LinkedTxnMixin,
    QuickbooksManagedObject,
    QuickbooksTransactionEntity,
    Ref,
)
from quickbooks.objects.detailline import AccountBasedExpenseLine, DetailLine, ItemBasedExpenseLine, TDSLine
from quickbooks.objects.tax import TxnTaxDetail


class Purchase(DeleteMixin, QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin):
    """
    QBO definition: This entity represents expenses, such as a purchase made from a vendor.
    There are three types of Purchases: Cash, Check, and Credit Card.

     - Cash Purchase contains information regarding a payment made in cash.
     - Check Purchase contains information regarding a payment made by check.
     - Credit Card Purchase contains information regarding a payment made by credit card or refunded/credited back
       to a credit card.

    For example, to create a transaction that sends a check to a vendor, create a Purchase object with PaymentType
    set to Check. To query Purchase transactions of a certain type, for example Check, submit the following to the
    query endpoint: SELECT * from Purchase where PaymentType='Check' You must specify an AccountRef for all purchases.
    The TotalAmtattribute must add up to sum of Line.Amount attributes.
    """

    class_dict: ClassVar[dict[str, type]] = {
        "AccountRef": Ref,
        "EntityRef": Ref,
        "DepartmentRef": Ref,
        "CurrencyRef": Ref,
        "PaymentMethodRef": Ref,
        "RemitToAddr": Address,
        "TxnTaxDetail": TxnTaxDetail,
    }

    list_dict: ClassVar[dict[str, type]] = {"Line": DetailLine, "LinkedTxn": LinkedTxn}

    detail_dict: ClassVar[dict[str, type]] = {
        "AccountBasedExpenseLineDetail": AccountBasedExpenseLine,
        "ItemBasedExpenseLineDetail": ItemBasedExpenseLine,
        "TDSLineDetail": TDSLine,
    }

    qbo_object_name = "Purchase"

    def __init__(self):
        super().__init__()
        self.DocNumber = ""
        self.TxnDate = ""
        self.ExchangeRate = 1
        self.PrivateNote = ""
        self.PaymentType = ""
        self.Credit = False
        self.TotalAmt = 0
        self.PrintStatus = "NeedToPrint"
        self.PurchaseEx = None
        self.TxnSource = None
        self.GlobalTaxCalculation = "TaxExcluded"

        self.TxnTaxDetail = None
        self.DepartmentRef = None
        self.AccountRef = None
        self.EntityRef = None
        self.CurrencyRef = None
        self.PaymentMethodRef = None
        self.RemitToAddr = None

        self.Line = []
        self.LinkedTxn = []

    def __str__(self):
        return str(self.TotalAmt)
