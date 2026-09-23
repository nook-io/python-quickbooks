from typing import ClassVar

from quickbooks.mixins import DeleteMixin
from quickbooks.objects.base import (
    AttachableRef,
    CustomField,
    LinkedTxn,
    LinkedTxnMixin,
    QuickbooksBaseObject,
    QuickbooksManagedObject,
    QuickbooksTransactionEntity,
    Ref,
)


class CashBackInfo(QuickbooksBaseObject):
    class_dict: ClassVar[dict[str, type]] = {"AccountRef": Ref}

    def __init__(self):
        super().__init__()
        self.Amount = 0
        self.Memo = ""
        self.AccountRef = None


class DepositLineDetail(QuickbooksBaseObject):
    class_dict: ClassVar[dict[str, type]] = {"Entity": Ref, "ClassRef": Ref, "AccountRef": Ref, "PaymentMethodRef": Ref}

    def __init__(self):
        super().__init__()
        self.CheckNum = ""
        self.TxnType = None

        self.Entity = None
        self.ClassRef = None
        self.AccountRef = None
        self.PaymentMethodRef = None


class DepositLine(QuickbooksBaseObject):
    class_dict: ClassVar[dict[str, type]] = {"DepositToAccountRef": Ref, "DepositLineDetail": DepositLineDetail}

    list_dict: ClassVar[dict[str, type]] = {"LinkedTxn": LinkedTxn, "CustomField": CustomField}

    qbo_object_name = "Deposit"

    def __init__(self):
        super().__init__()
        self.Id = None
        self.LineNum = 0
        self.Description = ""
        self.Amount = 0
        self.DetailType = "DepositLineDetail"
        self.LinkedTxn = []
        self.CustomField = []

    def __str__(self):
        return str(self.Amount)


class Deposit(DeleteMixin, QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin):
    """
    QBO definition: A deposit object is a transaction that records one or more deposits of the following types:

        -A customer payment, originally held in the Undeposited Funds account, into the Asset Account specified by
        the Deposit.DepositToAccountRef attribute. The Deposit.line.LinkedTxn sub-entity is used in this
        case to hold deposit information.

        -A new direct deposit specified by Deposit.Line.DepositLineDetail line detail.
    """

    class_dict: ClassVar[dict[str, type]] = {
        "DepositToAccountRef": Ref,
        "DepartmentRef": Ref,
        "CurrencyRef": Ref,
        "AttachableRef": AttachableRef,
        "CashBack": CashBackInfo,
    }

    list_dict: ClassVar[dict[str, type]] = {"Line": DepositLine}

    detail_dict: ClassVar[dict[str, type]] = {"DepositLineDetail": DepositLine}

    qbo_object_name = "Deposit"

    def __init__(self):
        super().__init__()
        self.TotalAmt = 0
        self.HomeTotalAmt = 0
        self.TxnDate = ""
        self.DocNumber = ""
        self.ExchangeRate = 1
        self.GlobalTaxCalculation = "TaxExcluded"
        self.PrivateNote = ""
        self.TxnStatus = ""
        self.TxnSource = None

        self.DepositToAccountRef = None
        self.DepartmentRef = None
        self.CurrencyRef = None
        self.AttachableRef = None
        self.Line = []

    def __str__(self):
        return str(self.TotalAmt)
