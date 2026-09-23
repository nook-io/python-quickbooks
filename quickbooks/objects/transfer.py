from typing import ClassVar

from quickbooks.mixins import DeleteMixin
from quickbooks.objects.base import LinkedTxnMixin, QuickbooksManagedObject, QuickbooksTransactionEntity, Ref


class Transfer(DeleteMixin, QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin):
    """
    QBO definition: A Transfer represents a transaction where funds are moved between two accounts from the
    company's QuickBooks chart of accounts.
    """

    class_dict: ClassVar[dict[str, type]] = {"FromAccountRef": Ref, "ToAccountRef": Ref}

    qbo_object_name = "Transfer"

    def __init__(self):
        super().__init__()
        self.Amount = 0
        self.TxnDate = None
        self.PrivateNote = None
        self.TxnSource = None

        self.FromAccountRef = None
        self.ToAccountRef = None

    def __str__(self):
        return str(self.Amount)
