from typing import ClassVar

from quickbooks.mixins import FromJsonMixin, ListMixin, ReadMixin, ToDictMixin, ToJsonMixin, UpdateMixin


class QuickbooksBaseObject(ToJsonMixin, FromJsonMixin, ToDictMixin):
    class_dict: ClassVar[dict[str, type]] = {}
    list_dict: ClassVar[dict[str, type]] = {}
    detail_dict: ClassVar[dict[str, type]] = {}


class QuickbooksTransactionEntity(QuickbooksBaseObject):
    def __init__(self):
        self.Id = None
        self.SyncToken = 0
        self.sparse = False
        self.domain = "QBO"


class QuickbooksManagedObject(QuickbooksBaseObject, ReadMixin, ListMixin, UpdateMixin):
    pass


class QuickbooksReadOnlyObject(QuickbooksBaseObject, ReadMixin, ListMixin):
    pass


class MetaData(FromJsonMixin):
    def __init__(self):
        self.CreateTime = ""
        self.LastUpdatedTime = ""

    def __str__(self):
        return f"Created {self.CreateTime}"


class LinkedTxnMixin:
    def to_linked_txn(self):
        linked_txn = LinkedTxn()
        linked_txn.TxnId = self.Id
        linked_txn.TxnType = self.qbo_object_name
        linked_txn.TxnLineId = 1

        return linked_txn


class Address(QuickbooksBaseObject):
    def __init__(self):
        self.Id = None
        self.Line1 = ""
        self.Line2 = ""
        self.Line3 = ""
        self.Line4 = ""
        self.Line5 = ""
        self.City = ""
        self.CountrySubDivisionCode = ""
        self.Country = ""
        self.PostalCode = ""
        self.Lat = ""
        self.Long = ""
        self.Note = ""

    def __str__(self):
        return f"{self.Line1} {self.City}, {self.CountrySubDivisionCode} {self.PostalCode}"


class PhoneNumber(ToJsonMixin, FromJsonMixin, ToDictMixin):
    def __init__(self):
        self.FreeFormNumber = ""

    def __str__(self):
        return self.FreeFormNumber


class EmailAddress(QuickbooksBaseObject):
    def __init__(self):
        self.Address = ""

    def __str__(self):
        return self.Address


class WebAddress(QuickbooksBaseObject):
    def __init__(self):
        self.URI = ""

    def __str__(self):
        return self.URI


class Ref(QuickbooksBaseObject):
    def __init__(self):
        self.value = ""
        self.name = ""
        self.type = ""

    def __str__(self):
        return self.name


class CustomField(QuickbooksBaseObject):
    def __init__(self):
        self.DefinitionId = ""
        self.Type = ""
        self.Name = ""
        self.StringValue = ""

    def __str__(self):
        return self.Name


class LinkedTxn(QuickbooksBaseObject):
    qbo_object_name = "LinkedTxn"

    def __init__(self):
        super().__init__()
        self.TxnId = 0
        self.TxnType = 0
        self.TxnLineId = 0

    def __str__(self):
        return str(self.TxnId)


class CustomerMemo(QuickbooksBaseObject):
    def __init__(self):
        super().__init__()
        self.value = ""

    def __str__(self):
        return self.value


class MarkupInfo(QuickbooksBaseObject):
    class_dict: ClassVar[dict[str, type]] = {"PriceLevelRef": Ref}

    def __init__(self):
        super().__init__()
        self.PercentBased = False
        self.Value = 0
        self.Percent = 0
        self.PriceLevelRef = None


class AttachableRef(QuickbooksBaseObject):
    class_dict: ClassVar[dict[str, type]] = {"EntityRef": Ref}

    list_dict: ClassVar[dict[str, type]] = {"CustomField": CustomField}

    qbo_object_name = "AttachableRef"

    def __init__(self):
        super().__init__()

        self.LineInfo = None
        self.IncludeOnSend = False
        self.Inactive = None
        self.NoRefOnly = None

        self.EntityRef = None
        self.CustomField = []
