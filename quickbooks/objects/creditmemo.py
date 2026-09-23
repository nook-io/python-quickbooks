from typing import ClassVar

from quickbooks.mixins import DeleteMixin
from quickbooks.objects.base import (
    Address,
    CustomerMemo,
    CustomField,
    EmailAddress,
    LinkedTxnMixin,
    QuickbooksManagedObject,
    QuickbooksTransactionEntity,
    Ref,
)
from quickbooks.objects.detailline import DescriptionOnlyLine, DetailLine, DiscountLine, SalesItemLine, SubtotalLine
from quickbooks.objects.tax import TxnTaxDetail


class CreditMemo(DeleteMixin, QuickbooksTransactionEntity, QuickbooksManagedObject, LinkedTxnMixin):
    """
    QBO definition: The CreditMemo is a financial transaction representing a refund or credit of payment or part
    of a payment for goods or services that have been sold.
    """

    class_dict: ClassVar[dict[str, type]] = {
        "BillAddr": Address,
        "ShipAddr": Address,
        "DepartmentRef": Ref,
        "ClassRef": Ref,
        "CustomerRef": Ref,
        "CurrencyRef": Ref,
        "SalesTermRef": Ref,
        "CustomerMemo": CustomerMemo,
        "BillEmail": EmailAddress,
        "TxnTaxDetail": TxnTaxDetail,
        "PaymentMethodRef": Ref,
        "DepositToAccountRef": Ref,
    }

    list_dict: ClassVar[dict[str, type]] = {"CustomField": CustomField, "Line": DetailLine}

    detail_dict: ClassVar[dict[str, type]] = {
        "SalesItemLineDetail": SalesItemLine,
        "SubTotalLineDetail": SubtotalLine,
        "DiscountLineDetail": DiscountLine,
        "DescriptionLineDetail": DescriptionOnlyLine,
    }

    qbo_object_name = "CreditMemo"

    def __init__(self):
        super().__init__()
        self.RemainingCredit = 0
        self.ExchangeRate = 0
        self.DocNumber = ""
        self.TxnDate = ""
        self.PrivateNote = ""
        self.TotalAmt = 0
        self.ApplyTaxAfterDiscount = ""
        self.PrintStatus = "NotSet"
        self.EmailStatus = "NotSet"
        self.Balance = 0
        self.GlobalTaxCalculation = "TaxExcluded"

        self.BillAddr = None
        self.ShipAddr = None
        self.ClassRef = None
        self.DepartmentRef = None
        self.CustomerRef = None
        self.CurrencyRef = None
        self.CustomerMemo = None
        self.BillEmail = None
        self.TxnTaxDetail = None
        self.SalesTermRef = None

        self.CustomField = []
        self.Line = []

    def __str__(self):
        return str(self.TotalAmt)
