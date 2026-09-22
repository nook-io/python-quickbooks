from typing import ClassVar

from quickbooks.objects.base import CustomField, LinkedTxn, MarkupInfo, QuickbooksBaseObject, Ref


class DetailLine(QuickbooksBaseObject):
    list_dict: ClassVar[dict[str, type]] = {"LinkedTxn": LinkedTxn, "CustomField": CustomField}

    def __init__(self):
        super().__init__()
        self.Id = None
        self.LineNum = 0
        self.Description = None
        self.Amount = 0
        self.DetailType = ""
        self.LinkedTxn = []
        self.CustomField = []

    def __str__(self):
        return f"[{self.LineNum}] {self.Description} {self.Amount}"


class DiscountOverride(QuickbooksBaseObject):
    class_dict: ClassVar[dict[str, type]] = {"DiscountRef": Ref, "DiscountAccountRef": Ref}

    qbo_object_name = "DiscountOverride"

    def __init__(self):
        super().__init__()
        self.PercentBased = False
        self.DiscountPercent = 0
        self.DiscountRef = None
        self.DiscountAccountRef = None


class DiscountLineDetail(QuickbooksBaseObject):
    class_dict: ClassVar[dict[str, type]] = {
        "Discount": DiscountOverride,
        "ClassRef": Ref,
        "TaxCodeRef": Ref,
        "DiscountAccountRef": Ref,
    }

    def __init__(self):
        super().__init__()

        self.Discount = None
        self.ClassRef = None
        self.TaxCodeRef = None
        self.PercentBased = False
        self.DiscountPercent = 0


class DiscountLine(DetailLine):
    class_dict: ClassVar[dict[str, type]] = {"DiscountLineDetail": DiscountLineDetail}

    def __init__(self):
        super().__init__()
        self.DetailType = "DiscountLineDetail"
        self.DiscountLineDetail = None


class SubtotalLineDetail(QuickbooksBaseObject):
    class_dict: ClassVar[dict[str, type]] = {"ItemRef": Ref}

    def __init__(self):
        super().__init__()
        self.ItemRef = None


class SubtotalLine(DetailLine):
    class_dict: ClassVar[dict[str, type]] = {"SubtotalLineDetail": SubtotalLineDetail}

    def __init__(self):
        super().__init__()
        self.DetailType = "SubTotalLineDetail"
        self.SubtotalLineDetail = None


class DescriptionLineDetail(QuickbooksBaseObject):
    class_dict: ClassVar[dict[str, type]] = {"TaxCodeRef": Ref}

    def __init__(self):
        super().__init__()
        self.ServiceDate = ""
        self.TaxCodeRef = None


class SalesItemLineDetail(QuickbooksBaseObject):
    class_dict: ClassVar[dict[str, type]] = {
        "ItemRef": Ref,
        "ClassRef": Ref,
        "TaxCodeRef": Ref,
        "PriceLevelRef": Ref,
        "MarkupInfo": MarkupInfo,
    }

    def __init__(self):
        super().__init__()
        self.UnitPrice = 0
        self.Qty = 0
        self.ServiceDate = ""
        self.TaxInclusiveAmt = 0

        self.MarkupInfo = None
        self.ItemRef = None
        self.ClassRef = None
        self.TaxCodeRef = None
        self.PriceLevelRef = None

    def __str__(self):
        return str(self.UnitPrice)


class SalesItemLine(DetailLine):
    class_dict: ClassVar[dict[str, type]] = {"SalesItemLineDetail": SalesItemLineDetail}

    def __init__(self):
        super().__init__()
        self.DetailType = "SalesItemLineDetail"
        self.SalesItemLineDetail = None


class GroupLineDetail(QuickbooksBaseObject):
    pass


class GroupLine(DetailLine):
    class_dict: ClassVar[dict[str, type]] = {"GroupLineDetail": GroupLineDetail}

    def __init__(self):
        super().__init__()
        self.DetailType = "GroupLineDetail"
        self.GroupLineDetail = None


class DescriptionOnlyLine(DetailLine):
    class_dict: ClassVar[dict[str, type]] = {"DescriptionLineDetail": DescriptionLineDetail}

    def __init__(self):
        super().__init__()
        self.DetailType = "DescriptionOnly"
        self.DescriptionLineDetail = None


class AccountBasedExpenseLineDetail(QuickbooksBaseObject):
    class_dict: ClassVar[dict[str, type]] = {
        "CustomerRef": Ref,
        "AccountRef": Ref,
        "TaxCodeRef": Ref,
        "ClassRef": Ref,
        "MarkupInfo": MarkupInfo,
    }

    def __init__(self):
        super().__init__()
        self.BillableStatus = None
        self.TaxAmount = 0
        self.TaxInclusiveAmt = 0

        self.CustomerRef = None
        self.AccountRef = None
        self.TaxCodeRef = None

    def __str__(self):
        return self.BillableStatus


class AccountBasedExpenseLine(DetailLine):
    class_dict: ClassVar[dict[str, type]] = {"AccountBasedExpenseLineDetail": AccountBasedExpenseLineDetail}

    def __init__(self):
        super().__init__()

        self.DetailType = "AccountBasedExpenseLineDetail"
        self.AccountBasedExpenseLineDetail = None


class TDSLineDetail(QuickbooksBaseObject):
    def __init__(self):
        super().__init__()
        self.TDSSectionTypeId = None

    def __str__(self):
        return self.TDSSectionTypeId


class TDSLine(DetailLine):
    class_dict: ClassVar[dict[str, type]] = {"TDSLineDetail": TDSLineDetail}

    def __init__(self):
        super().__init__()

        self.DetailType = "TDSLineDetail"
        self.TDSLineDetail = None


class ItemBasedExpenseLineDetail(QuickbooksBaseObject):
    class_dict: ClassVar[dict[str, type]] = {
        "ItemRef": Ref,
        "ClassRef": Ref,
        "PriceLevelRef": Ref,
        "TaxCodeRef": Ref,
        "CustomerRef": Ref,
        "MarkupInfo": MarkupInfo,
    }

    def __init__(self):
        super().__init__()
        self.BillableStatus = None
        self.UnitPrice = 0
        self.TaxInclusiveAmt = 0
        self.Qty = 0
        self.ItemRef = None
        self.ClassRef = None
        self.PriceLevelRef = None
        self.TaxCodeRef = None
        self.MarkupInfo = None
        self.CustomerRef = None


class ItemBasedExpenseLine(DetailLine):
    class_dict: ClassVar[dict[str, type]] = {"ItemBasedExpenseLineDetail": ItemBasedExpenseLineDetail}

    def __init__(self):
        super().__init__()

        self.DetailType = "ItemBasedExpenseLineDetail"
        self.ItemBasedExpenseLineDetail = None
