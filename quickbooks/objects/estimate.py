from typing import ClassVar

from quickbooks.mixins import DeleteMixin, QuickbooksPdfDownloadable, SendMixin
from quickbooks.objects.base import (
    Address,
    CustomerMemo,
    CustomField,
    EmailAddress,
    LinkedTxn,
    LinkedTxnMixin,
    QuickbooksManagedObject,
    QuickbooksTransactionEntity,
    Ref,
)
from quickbooks.objects.detailline import (
    DescriptionOnlyLine,
    DetailLine,
    DiscountLine,
    GroupLine,
    SalesItemLine,
    SubtotalLine,
)
from quickbooks.objects.tax import TxnTaxDetail


class Estimate(
    DeleteMixin,
    QuickbooksPdfDownloadable,
    QuickbooksManagedObject,
    QuickbooksTransactionEntity,
    LinkedTxnMixin,
    SendMixin,
):
    """
    QBO definition: The Estimate represents a proposal for a financial transaction from a business to a customer
    for goods or services proposed to be sold, including proposed pricing.
    """

    class_dict: ClassVar[dict[str, type]] = {
        "BillAddr": Address,
        "ShipAddr": Address,
        "CustomerRef": Ref,
        "TxnTaxDetail": TxnTaxDetail,
        "CustomerMemo": CustomerMemo,
        "BillEmail": EmailAddress,
        "DepartmentRef": Ref,
        "CurrencyRef": Ref,
        "ClassRef": Ref,
        "SalesTermRef": Ref,
        "ShipMethodRef": Ref,
    }

    list_dict: ClassVar[dict[str, type]] = {"CustomField": CustomField, "LinkedTxn": LinkedTxn, "Line": DetailLine}

    detail_dict: ClassVar[dict[str, type]] = {
        "SalesItemLineDetail": SalesItemLine,
        "GroupLineDetail": GroupLine,
        "DescriptionOnly": DescriptionOnlyLine,
        "DiscountLineDetail": DiscountLine,
        "SubTotalLineDetail": SubtotalLine,
    }

    qbo_object_name = "Estimate"

    def __init__(self):
        super().__init__()
        self.DocNumber = None
        self.TxnDate = None
        self.TxnStatus = None
        self.PrivateNote = None
        self.TotalAmt = 0
        self.ExchangeRate = 1
        self.ApplyTaxAfterDiscount = False
        self.PrintStatus = "NotSet"
        self.EmailStatus = "NotSet"
        self.DueDate = None
        self.ShipDate = None
        self.ExpirationDate = None
        self.AcceptedBy = None
        self.AcceptedDate = None
        self.GlobalTaxCalculation = "TaxExcluded"
        self.BillAddr = None
        self.ShipAddr = None
        self.BillEmail = None
        self.CustomerRef = None
        self.TxnTaxDetail = None
        self.CustomerMemo = None
        self.ClassRef = None
        self.SalesTermRef = None
        self.ShipMethodRef = None

        self.CustomField = []
        self.LinkedTxn = []
        self.Line = []

    def __str__(self):
        return str(self.TotalAmt)
