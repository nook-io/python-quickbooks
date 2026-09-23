import base64
import hashlib
import hmac
import http.client as httplib
import json
import textwrap
import warnings
from typing import ClassVar

from requests_oauthlib import OAuth2Session

from quickbooks import exceptions


def to_bytes(value, *args, **kwargs):
    return bytes(value, "utf-8", *args, **kwargs)


class Environments:
    SANDBOX = "sandbox"
    PRODUCTION = "production"


class QuickBooks:
    company_id = 0
    session = None
    auth_client = None
    sandbox = False
    minorversion = None
    verifier_token = None
    invoice_link = False

    sandbox_api_url_v3 = "https://sandbox-quickbooks.api.intuit.com/v3"
    api_url_v3 = "https://quickbooks.api.intuit.com/v3"
    current_user_url = "https://appcenter.intuit.com/api/v1/user/current"

    _BUSINESS_OBJECTS: ClassVar[list[str]] = [
        "Account",
        "Attachable",
        "Bill",
        "BillPayment",
        "Class",
        "CreditMemo",
        "Customer",
        "CompanyCurrency",
        "Department",
        "Deposit",
        "Employee",
        "Estimate",
        "ExchangeRate",
        "Invoice",
        "Item",
        "JournalEntry",
        "Payment",
        "PaymentMethod",
        "Preferences",
        "Purchase",
        "PurchaseOrder",
        "RefundReceipt",
        "SalesReceipt",
        "TaxAgency",
        "TaxCode",
        "TaxService/Taxcode",
        "TaxRate",
        "Term",
        "TimeActivity",
        "Transfer",
        "Vendor",
        "VendorCredit",
        "CreditCardPayment",
    ]

    __instance = None
    __use_global = False

    def __new__(cls, **kwargs):
        """
        If global is disabled, don't set global client instance.
        """
        if QuickBooks.__use_global:
            if QuickBooks.__instance is None:
                QuickBooks.__instance = object.__new__(cls)
            instance = QuickBooks.__instance
        else:
            instance = object.__new__(cls)

        if "refresh_token" in kwargs:
            instance.refresh_token = kwargs["refresh_token"]

        if "auth_client" in kwargs:
            instance.auth_client = kwargs["auth_client"]

            if instance.auth_client.environment == Environments.SANDBOX:
                instance.sandbox = True
            else:
                instance.sandbox = False

            refresh_token = instance._start_session()
            instance.refresh_token = refresh_token

        if "company_id" in kwargs:
            instance.company_id = kwargs["company_id"]

        if "minorversion" in kwargs:
            instance.minorversion = kwargs["minorversion"]

        instance.invoice_link = kwargs.get("invoice_link", False)

        if "verifier_token" in kwargs:
            instance.verifier_token = kwargs.get("verifier_token")

        return instance

    def _start_session(self):
        if self.auth_client.access_token is None:
            self.auth_client.refresh(refresh_token=self.refresh_token)

        self.session = OAuth2Session(
            self.auth_client.client_id,
            token={"access_token": self.auth_client.access_token, "refresh_token": self.auth_client.refresh_token},
        )
        return self.auth_client.refresh_token

    @classmethod
    def get_instance(cls):
        return cls.__instance

    @classmethod
    def disable_global(cls):
        """
        Disable use of singleton pattern.
        """
        warnings.warn("disable_global deprecated", PendingDeprecationWarning, stacklevel=2)
        QuickBooks.__use_global = False
        QuickBooks.__instance = None

    @classmethod
    def enable_global(cls):
        """
        Allow use of singleton pattern.
        """
        warnings.warn("enable_global deprecated", PendingDeprecationWarning, stacklevel=2)
        QuickBooks.__use_global = True

    def _drop(self):
        QuickBooks.__instance = None

    @property
    def api_url(self):
        if self.sandbox:
            return self.sandbox_api_url_v3
        return self.api_url_v3

    def validate_webhook_signature(self, request_body, signature, verifier_token=None):
        hmac_verifier_token_hash = hmac.new(
            to_bytes(verifier_token or self.verifier_token), request_body.encode("utf-8"), hashlib.sha256
        ).digest()
        decoded_hex_signature = base64.b64decode(signature)
        return hmac_verifier_token_hash == decoded_hex_signature

    def get_current_user(self):
        """Get data from the current user endpoint"""
        url = self.current_user_url
        return self.get(url)

    def get_report(self, report_type, qs=None):
        """Get data from the report endpoint"""
        if qs is None:
            qs = {}

        url = self.api_url + f"/company/{self.company_id}/reports/{report_type}"
        return self.get(url, params=qs)

    def change_data_capture(self, entity_string, changed_since):
        url = f"{self.api_url}/company/{self.company_id}/cdc"

        params = {"entities": entity_string, "changedSince": changed_since}

        return self.get(url, params=params)

    def make_request(
        self,
        request_type,
        url,
        request_body=None,
        content_type="application/json",
        params=None,
        file_path=None,
        request_id=None,
        file_data=None,
    ):
        if not params:
            params = {}

        if self.minorversion:
            params["minorversion"] = self.minorversion

        if request_id:
            params["requestid"] = request_id

        if self.invoice_link:
            params["include"] = "invoiceLink"

        if not request_body:
            request_body = {}

        headers = {
            "Content-Type": content_type,
            "Accept": "application/json",
            "User-Agent": "python-quickbooks V3 library",
        }

        if file_path or file_data:
            attachment = open(file_path, "rb") if not file_data else file_data
            url = url.replace("attachable", "upload")
            boundary = "-------------PythonMultipartPost"
            headers.update(
                {
                    "Content-Type": f"multipart/form-data; boundary={boundary}",
                    "Accept-Encoding": "gzip;q=1.0,deflate;q=0.6,identity;q=0.3",
                    "User-Agent": "python-quickbooks V3 library",
                    "Accept": "application/json",
                    "Connection": "close",
                }
            )

            binary_data = str(base64.b64encode(attachment.read() if not file_data else file_data).decode("ascii"))

            content_type = json.loads(request_body)["ContentType"]

            request_body = textwrap.dedent(
                """
                --%s
                Content-Disposition: form-data; name="file_metadata_01"
                Content-Type: application/json

                %s

                --%s
                Content-Disposition: form-data; name="file_content_01"
                Content-Type: %s
                Content-Transfer-Encoding: base64

                %s

                --%s--
                """
            ) % (boundary, request_body, boundary, content_type, binary_data, boundary)

            request_body = str(request_body)

        req = self.process_request(request_type, url, headers=headers, params=params, data=request_body)

        if req.status_code == httplib.UNAUTHORIZED:
            raise exceptions.AuthorizationException(
                "Application authentication failed", error_code=req.status_code, detail=req.text
            )

        try:
            result = req.json()
        except Exception as exc:
            raise exceptions.QuickbooksException(f"Error reading json response: {req.text}", 10000) from exc

        if "Fault" in result:
            self.handle_exceptions(result["Fault"])
        elif not req.status_code == httplib.OK:
            raise exceptions.QuickbooksException(
                f"Error returned with status code '{req.status_code}': {req.text}", 10000
            )
        else:
            return result
        return None

    def get(self, *args, **kwargs):
        return self.make_request("GET", *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.make_request("POST", *args, **kwargs)

    def process_request(self, request_type, url, headers="", params="", data=""):
        if self.session is None:
            raise exceptions.QuickbooksException("No session manager")

        headers.update({"Authorization": "Bearer " + self.session.access_token})

        return self.session.request(request_type, url, headers=headers, params=params, data=data)

    def get_single_object(self, qbbo, pk):
        url = f"{self.api_url}/company/{self.company_id}/{qbbo.lower()}/{pk}/"
        return self.get(url, {})

    @staticmethod
    def handle_exceptions(results):
        """
        Error codes with description in documentation:
        https://developer.intuit.com/app/developer/qbo/docs/develop/troubleshooting/error-codes#id1
        """
        # Needs to handle multiple errors
        for error in results["Error"]:
            message = error["Message"]

            detail = ""
            if "Detail" in error:
                detail = error["Detail"]

            code = ""
            if "code" in error:
                code = int(error["code"])

            if 0 < code <= 499:
                raise exceptions.AuthorizationException(message, code, detail)
            if 500 <= code <= 599:
                raise exceptions.UnsupportedException(message, code, detail)
            if 600 <= code <= 1999:
                if code == 610:
                    raise exceptions.ObjectNotFoundException(message, code, detail)
                raise exceptions.GeneralException(message, code, detail)
            if 2000 <= code <= 4999:
                raise exceptions.ValidationException(message, code, detail)
            if 10000 <= code:
                raise exceptions.SevereException(message, code, detail)
            raise exceptions.QuickbooksException(message, code, detail)

    def create_object(self, qbbo, request_body, _file_path=None, request_id=None, _file_data=None):
        self.isvalid_object_name(qbbo)

        url = f"{self.api_url}/company/{self.company_id}/{qbbo.lower()}"
        return self.post(url, request_body, file_path=_file_path, request_id=request_id, file_data=_file_data)

    def query(self, select):
        url = f"{self.api_url}/company/{self.company_id}/query"
        return self.post(url, select, content_type="application/text")

    def isvalid_object_name(self, object_name):
        if object_name not in self._BUSINESS_OBJECTS:
            raise Exception(f"{object_name} is not a valid QBO Business Object.")

        return True

    def update_object(self, qbbo, request_body, _file_path=None, request_id=None, _file_data=None):
        url = f"{self.api_url}/company/{self.company_id}/{qbbo.lower()}"
        return self.post(url, request_body, file_path=_file_path, request_id=request_id, file_data=_file_data)

    def delete_object(self, qbbo, request_body, _file_path=None, request_id=None, _file_data=None):
        url = f"{self.api_url}/company/{self.company_id}/{qbbo.lower()}"
        return self.post(
            url,
            request_body,
            params={"operation": "delete"},
            file_path=_file_path,
            request_id=request_id,
            file_data=_file_data,
        )

    def batch_operation(self, request_body):
        url = f"{self.api_url}/company/{self.company_id}/batch"
        return self.post(url, request_body)

    def misc_operation(self, end_point, request_body, content_type="application/json"):
        url = f"{self.api_url}/company/{self.company_id}/{end_point}"
        return self.post(url, request_body, content_type)

    def download_pdf(self, qbbo, item_id):
        if self.session is None:
            raise exceptions.QuickbooksException("No session")

        url = f"{self.api_url}/company/{self.company_id}/{qbbo.lower()}/{item_id}/pdf"

        headers = {
            "Content-Type": "application/pdf",
            "Accept": "application/pdf, application/json",
            "User-Agent": "python-quickbooks V3 library",
        }

        response = self.process_request("GET", url, headers=headers)

        if response.status_code != httplib.OK:
            if response.status_code == httplib.UNAUTHORIZED:
                # Note that auth errors have different result structure which can't be parsed by handle_exceptions()
                raise exceptions.AuthorizationException(
                    "Application authentication failed", error_code=response.status_code, detail=response.text
                )

            try:
                result = response.json()
            except Exception as exc:
                raise exceptions.QuickbooksException(f"Error reading json response: {response.text}", 10000) from exc

            self.handle_exceptions(result["Fault"])
        else:
            return response.content
        return None


def revoke_token(self, refresh_token=None):

    if not self.auth_client:
        raise exceptions.QuickbooksException("No auth_client available for token revocation")

    token_to_revoke = refresh_token or getattr(self, "refresh_token", None)

    if not token_to_revoke:
        raise exceptions.QuickbooksException("No refresh token available for revocation")

    try:
        self.auth_client.revoke(token_to_revoke)
    except Exception as e:
        print(f"Failed to revoke QuickBooks OAuth token: {e!s}")
        return False
    else:
        return True
