class OAuth:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

    def app_description(self):
        return {
            "name": "xero",
            "version": "2",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "endpoint_url": "https://api.xero.com/",
            "authorization_url": "https://login.xero.com/identity/connect/authorize",
            "access_token_url": "https://identity.xero.com/connect/token",
            "refresh_token_url": "https://identity.xero.com/connect/token",
            "scope": "offline_access openid profile email accounting.transactions "
                    "accounting.reports.read accounting.journals.read accounting.settings "
                    "accounting.contacts accounting.attachments assets projects",
        }
