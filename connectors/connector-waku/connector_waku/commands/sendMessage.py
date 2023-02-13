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
    recipient: list[str]

    def send_message(self, message_type_to_use: str, rec: str, message_to_send: str) -> None:
        url = f'{current_app.config["WAKU_BASE_URL"]}'
        headers = {"Accept": "application/json", "Content-type": "application/json"}
        request_body = {
            "jsonrpc": "2.0",
            "method": message_type_to_use,
            "params": [{"id": rec, "message": message_to_send}],
            "id": 1,
        }

        try:
            raw_response = requests.post(url, json.dumps(request_body), headers=headers)
            status_code = raw_response.status_code
            parsed_response = json.loads(raw_response.text)
            response = parsed_response
        except Exception as ex:
            response = {"error": str(ex)}
            status_code = 500
        return (response, status_code)

    def execute(self, config, task_data):
        """Execute."""
        responses = []
        all_calls_returned_200 = True
        for rec in self.recipient:
            response, status_code = self.send_message('wakuext_sendContactRequest', rec, 'Contact Request')
            if status_code == 200:
                response, status_code = self.send_message(self.message_type, rec, self.message)
            if status_code != 200:
                all_calls_returned_200 = False

            responses.append({
                "response": response,
                "status": status_code,
            })
        return ({
            "response": json.dumps(responses),
            "node_returned_200": all_calls_returned_200,
            "status": 200,
            "mimetype": "application/json",
        })
