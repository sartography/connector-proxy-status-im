import json
import requests
from dataclasses import dataclass
from flask import current_app


@dataclass
class SendMessage:
    message: str
    message_type: str
    recipient: str

    def execute(self, config, task_data):
        url = f'{current_app.config["WAKU_PROXY_BASE_URL"]}/sendMessage'
        headers = {'Accept': 'application/json', 'Content-type': 'application/json'}
        request_body = {"message": self.message, "recipient": self.recipient, "message_type": self.message_type}

        status_code = None
        try:
            raw_response = requests.post(url, json.dumps(request_body), headers=headers)
            status_code = raw_response.status_code
            parsed_response = json.loads(raw_response.text)
            response = json.dumps(parsed_response)
        except Exception as ex:
            response = json.dumps({"error": str(ex)})

        return {
            'response': response,
            'node_returned_200': True,
            'status': status_code,
            'mimetype': 'application/json'
        }
