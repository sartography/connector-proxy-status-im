"""GetCurrencies."""
import json

from xero_python.accounting import AccountingApi  # type: ignore
from xero_python.api_client import ApiClient  # type: ignore
from xero_python.api_client.configuration import Configuration  # type: ignore
from xero_python.api_client.oauth2 import OAuth2Token  # type: ignore
from xero_python.api_client.serializer import serialize  # type: ignore
from xero_python.identity import IdentityApi  # type: ignore

#
# Sample response
#

#	{
#	  "Id": "37047def-f1c5-4fb0-85a3-c20a6259a52a",
#	  "Status": "OK",
#	  "ProviderName": "API Explorer",
#	  "DateTimeUTC": "\/Date(1673367618959)\/",
#	  "Currencies": [
#	    {
#	      "Code": "CHF",
#	      "Description": "Swiss Franc"
#	    }
#	  ]
#	}


class GetCurrencies:
    """GetCurrencies."""

    def __init__(self, access_token):
        """__init__."""
        self.access_token = access_token

    def execute(self, config, task_data):
        """Get currencies configured in xero."""
        client_id = config["XERO_CLIENT_ID"]
        client_secret = config["XERO_CLIENT_SECRET"]

        # this should be called token_set to match the docs
        access_token = json.loads(self.access_token)

        # need a mutable "store" to appease the libs
        token_store = {}
        token_store_key = "token"

        api_client = ApiClient(
            Configuration(
                debug=True,
                oauth2_token=OAuth2Token(
                    client_id=client_id, client_secret=client_secret
                ),
            ),
            pool_threads=1,
        )

        @api_client.oauth2_token_getter
        def obtain_xero_oauth2_token():
            """Obtain_xero_oauth2_token."""
            return token_store[token_store_key]

        @api_client.oauth2_token_saver
        def store_xero_oauth2_token(token):
            """Store_xero_oauth2_token."""
            token_store[token_store_key] = token  # noqa

        store_xero_oauth2_token(access_token)

        api_client.refresh_oauth2_token()

        api_instance = AccountingApi(api_client)

        try:
            xero_tenant_id = self._get_xero_tenant_id(api_client, access_token)
            currencies = api_instance.get_currencies(
                xero_tenant_id, "", "Code ASC"
            )
            response = json.dumps(
                {
                    "api_response": serialize(currencies),
                    "refreshed_token_set": obtain_xero_oauth2_token(),
                    "auth": "xero/OAuth",
                }
            )
            status = 200
        except Exception as e:
            # TODO better error logging/reporting in debug
            response = f'{{ "error": "{e.reason}" }}'
            status = 500

        return {"response": response, "status": status, "mimetype": "application/json"}

    def _get_xero_tenant_id(self, api_client, token):
        """_get_xero_tenant_id."""
        if not token:
            return None

        identity_api = IdentityApi(api_client)
        for connection in identity_api.get_connections():
            if connection.tenant_type == "ORGANISATION":
                return connection.tenant_id
