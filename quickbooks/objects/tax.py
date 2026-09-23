from typing import ClassVar

from quickbooks.objects.base import QuickbooksBaseObject, Ref


class TaxLineDetail(QuickbooksBaseObject):
    class_dict: ClassVar[dict[str, type]] = {"TaxRateRef": Ref}

    def __init__(self):
        super().__init__()
        self.PercentBased = True
        self.TaxPercent = 0
        self.NetAmountTaxable = 0

    def __str__(self):
        return str(self.TaxPercent)


class TaxLine(QuickbooksBaseObject):
    class_dict: ClassVar[dict[str, type]] = {"TaxLineDetail": TaxLineDetail}

    def __init__(self):
        super().__init__()
        self.Amount = 0
        self.DetailType = ""

    def __str__(self):
        return str(self.Amount)


class TxnTaxDetail(QuickbooksBaseObject):
    class_dict: ClassVar[dict[str, type]] = {"TxnTaxCodeRef": Ref}

    list_dict: ClassVar[dict[str, type]] = {"TaxLine": TaxLine}

    def __init__(self):
        super().__init__()
        self.TotalTax = 0
        self.TxnTaxCodeRef = None
        self.TaxLine = []

    def __str__(self):
        return str(self.TotalTax)
