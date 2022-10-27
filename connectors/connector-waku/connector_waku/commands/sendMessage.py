"""SendMessage."""
import json
from dataclasses import dataclass

import requests
from flask import current_app


# Example:
"""
curl -XPOST http://localhost:8545 -H 'Content-type: application/json' \
    '{
     "jsonrpc": "2.0",
     "method": "wakuext_sendOneToOneMessage",
     "params": [
         {
         "id": "0xPUBLIC_KEY",
         "message": "hello there, try http://167.172.242.138:7001/"
         }
     ],
     "id": 1
     }'
"""


@dataclass
class SendMessage:
    """SendMessage."""

    message: str
    message_type: str
    recipient: str

    def execute(self, config, task_data):
        """Execute."""
        url = f'{current_app.config["WAKU_BASE_URL"]}'
        headers = {"Accept": "application/json", "Content-type": "application/json"}
        request_body = {
            "jsonrpc": "2.0",
            "method": self.message_type,
            "params": [{"id": self.recipient, "message": self.message}],
            "id": 1,
        }

        status_code = 0
        try:
            raw_response = requests.post(url, json.dumps(request_body), headers=headers)
            status_code = raw_response.status_code
            parsed_response = json.loads(raw_response.text)
            response = json.dumps(parsed_response)
        except Exception as ex:
            response = json.dumps({"error": str(ex)})
            status_code = 500

        return {
            "response": response,
            "node_returned_200": True,
            "status": status_code,
            "mimetype": "application/json",
        }
