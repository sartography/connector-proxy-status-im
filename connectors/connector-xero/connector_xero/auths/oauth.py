"""Oauth."""


class OAuth:
    """OAuth."""

    def __init__(self):
        """init."""
        pass

    def app_description(self, config):
        """App_description."""
        return {
            "name": "xero",
            "version": "2",
            "client_id": config["XERO_CLIENT_ID"],
            "client_secret": config["XERO_CLIENT_SECRET"],
            "endpoint_url": "https://api.xero.com/",
            "authorization_url": "https://login.xero.com/identity/connect/authorize",
            "access_token_url": "https://identity.xero.com/connect/token",
            "refresh_token_url": "https://identity.xero.com/connect/token",
            "scope": "offline_access openid profile email accounting.transactions "
            "accounting.reports.read accounting.journals.read accounting.settings "
            "accounting.contacts accounting.attachments assets projects",
        }

    # TODO reconsider how this is working
    @staticmethod
    def filtered_params(params):
        """Filtered_params."""
        return {
            "client_id": params["client_id"],
            "client_secret": params["client_secret"],
        }
