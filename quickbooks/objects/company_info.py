from typing import ClassVar

from quickbooks.objects.base import Address, EmailAddress, PhoneNumber, QuickbooksReadOnlyObject, Ref, WebAddress


class CompanyInfo(QuickbooksReadOnlyObject):
    """
    QBO definition: The CompanyInfo entity contains basic company information.
    In QuickBooks Online, company info and preferences are displayed in the
    same place under preferences, so it may be confusing to figure out from
    user interface which fields may belong to this entity. But in general,
    properties such as company addresses or name are considered company
    information. Some attributes may exist in both CompanyInfo and Preferences
    entities.
    """

    class_dict: ClassVar[dict[str, type]] = {
        "CompanyAddr": Address,
        "CustomerCommunicationAddr": Address,
        "LegalAddr": Address,
        "PrimaryPhone": PhoneNumber,
        "Email": EmailAddress,
        "WebAddr": WebAddress,
    }

    qbo_object_name = "CompanyInfo"

    def __init__(self):
        super().__init__()

        self.Id = None
        self.CompanyName = ""
        self.LegalName = ""
        self.CompanyStartDate = ""
        self.FiscalYearStartMonth = ""
        self.Country = ""
        self.SupportedLanguages = ""

        self.CompanyAddr = None
        self.CustomerCommunicationAddr = None
        self.LegalAddr = None
        self.PrimaryPhone = None
        self.Email = None
        self.WebAddr = None

    def __str__(self):
        return self.CompanyName

    def to_ref(self):
        ref = Ref()

        ref.name = self.CompanyName
        ref.type = self.qbo_object_name
        ref.value = self.Id

        return ref
