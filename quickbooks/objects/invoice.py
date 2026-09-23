from typing import ClassVar

from quickbooks.mixins import DeleteMixin, QuickbooksPdfDownloadable, SendMixin, VoidMixin
from quickbooks.objects.base import (
    Address,
    CustomerMemo,
    CustomField,
    EmailAddress,
    LinkedTxn,
    LinkedTxnMixin,
    QuickbooksBaseObject,
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


class DeliveryInfo(QuickbooksBaseObject):
    def __init__(self):
        super().__init__()
        self.DeliveryType = ""
        self.DeliveryTime = ""


class Invoice(
    DeleteMixin,
    QuickbooksPdfDownloadable,
    QuickbooksManagedObject,
    QuickbooksTransactionEntity,
    LinkedTxnMixin,
    SendMixin,
    VoidMixin,
):
    """
    QBO definition: An Invoice represents a sales form where the customer pays for a product or service later.

    """

    class_dict: ClassVar[dict[str, type]] = {
        "DepartmentRef": Ref,
        "CurrencyRef": Ref,
        "CustomerRef": Ref,
        "ClassRef": Ref,
        "SalesTermRef": Ref,
        "ShipMethodRef": Ref,
        "DepositToAccountRef": Ref,
        "BillAddr": Address,
        "ShipAddr": Address,
        "TxnTaxDetail": TxnTaxDetail,
        "BillEmail": EmailAddress,
        "CustomerMemo": CustomerMemo,
        "DeliveryInfo": DeliveryInfo,
    }

    list_dict: ClassVar[dict[str, type]] = {"CustomField": CustomField, "Line": DetailLine, "LinkedTxn": LinkedTxn}

    detail_dict: ClassVar[dict[str, type]] = {
        "SalesItemLineDetail": SalesItemLine,
        "SubTotalLineDetail": SubtotalLine,
        "DiscountLineDetail": DiscountLine,
        "DescriptionOnly": DescriptionOnlyLine,
        "GroupLineDetail": GroupLine,
    }

    qbo_object_name = "Invoice"

    def __init__(self):
        super().__init__()
        self.Deposit = 0
        self.Balance = 0
        self.AllowIPNPayment = True
        self.AllowOnlineCreditCardPayment = False
        self.AllowOnlineACHPayment = False
        self.DocNumber = None

        self.PrivateNote = ""
        self.DueDate = ""
        self.ShipDate = ""
        self.TrackingNum = ""
        self.TotalAmt = ""
        self.TxnDate = ""
        self.ApplyTaxAfterDiscount = False
        self.PrintStatus = "NotSet"
        self.EmailStatus = "NotSet"
        self.ExchangeRate = 1
        self.GlobalTaxCalculation = "TaxExcluded"
        self.InvoiceLink = ""

        self.EInvoiceStatus = None

        self.BillAddr = None
        self.ShipAddr = None
        self.BillEmail = None
        self.CustomerRef = None
        self.CurrencyRef = None
        self.CustomerMemo = None
        self.DepartmentRef = None
        self.TxnTaxDetail = None
        self.DeliveryInfo = None

        self.CustomField = []
        self.Line = []
        self.LinkedTxn = []

    def __str__(self):
        return str(self.TotalAmt)

    def to_linked_txn(self):
        linked_txn = LinkedTxn()
        linked_txn.TxnId = self.Id
        linked_txn.TxnType = "Invoice"
        linked_txn.TxnLineId = 1

        return linked_txn

    @property
    def email_sent(self):
        if self.EmailStatus == "EmailSent":
            return True

        return False

    def to_ref(self):
        ref = Ref()

        ref.name = self.DocNumber
        ref.type = self.qbo_object_name
        ref.value = self.Id

        return ref
