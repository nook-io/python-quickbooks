from typing import ClassVar

from quickbooks.objects.base import QuickbooksManagedObject, QuickbooksTransactionEntity


class TaxAgency(QuickbooksManagedObject, QuickbooksTransactionEntity):
    """
    QBO definition: Tax Agency is an entity that is associated with a tax rate and identifies the agency to which that tax rate
    applies, that is, the entity that collects those taxes.
    """

    class_dict: ClassVar[dict[str, type]] = {}

    qbo_object_name = "TaxAgency"

    def __init__(self):
        super().__init__()
        self.DisplayName = ""
        self.TaxRegistrationNumber = ""
        self.TaxTrackedOnSales = True
        self.TaxTrackedOnPurchases = False

    def __str__(self):
        return self.DisplayName
