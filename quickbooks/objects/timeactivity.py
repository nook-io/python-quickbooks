from typing import ClassVar

from quickbooks.mixins import DeleteMixin
from quickbooks.objects.base import (
    AttachableRef,
    LinkedTxnMixin,
    QuickbooksManagedObject,
    QuickbooksTransactionEntity,
    Ref,
)


class TimeActivity(DeleteMixin, QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin):
    """
    QBO definition: The TimeActivity entity represents a record of time worked by a vendor or employee.
    """

    class_dict: ClassVar[dict[str, type]] = {
        "VendorRef": Ref,
        "CustomerRef": Ref,
        "DepartmentRef": Ref,
        "EmployeeRef": Ref,
        "ItemRef": Ref,
        "ClassRef": Ref,
        "AttachableRef": AttachableRef,
    }

    qbo_object_name = "TimeActivity"

    def __init__(self):
        super().__init__()
        self.NameOf = ""  # required
        self.TxnDate = None
        self.BillableStatus = None
        self.Taxable = False
        self.HourlyRate = None
        self.Hours = None
        self.Minutes = None
        self.BreakHours = None
        self.BreakMinutes = None
        self.StartTime = None
        self.EndTime = None
        self.Description = None

        self.VendorRef = None
        self.CustomerRef = None
        self.DepartmentRef = None
        self.EmployeeRef = None
        self.ItemRef = None
        self.ClassRef = None
        self.AttachableRef = None

    def __str__(self):
        return self.NameOf
