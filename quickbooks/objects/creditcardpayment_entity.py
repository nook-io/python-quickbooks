from typing import ClassVar

from quickbooks.mixins import DeleteMixin
from quickbooks.objects.base import LinkedTxnMixin, QuickbooksManagedObject, QuickbooksTransactionEntity, Ref


class CreditCardPayment(DeleteMixin, QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin):
    """
    QBO definition: A Represents a financial transaction to record a Credit Card balance payment
    in QuickBooks Online. It provides an easy way for users to move money from a Bank account to
    a Credit Card account. It is essentially a more limited Transfer form.

    Added in QuickBooks Online v1928, Date: February 13, 2020

    https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/creditcardpayment
    """

    class_dict: ClassVar[dict[str, type]] = {"BankAccountRef": Ref, "CreditCardAccountRef": Ref}

    qbo_object_name = "CreditCardPayment"
    qbo_json_object_name = "CreditCardPaymentTxn"  # JSON object name doesn't match the endpoint name - Thanks Intuit!

    def __init__(self):
        super().__init__()
        self.TxnDate = None
        self.Amount = 0
        self.PrivateNote = None

        self.BankAccountRef = None
        self.CreditCardAccountRef = None

    def __str__(self):
        return str(self.Amount)
