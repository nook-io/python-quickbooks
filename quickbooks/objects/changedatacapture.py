from quickbooks.mixins import FromJsonMixin, ObjectListMixin


class CDCResponse(FromJsonMixin):
    qbo_object_name = "CDCResponse"

    def __init__(self):
        super().__init__()


class QueryResponse(FromJsonMixin, ObjectListMixin):
    qbo_object_name = "QueryResponse"

    def __init__(self):
        super().__init__()
