import json
import requests

#
# Sample response
#

# {
#    "amount": "65000.00",
#    "currency": "USD",
#    "id": "4",
#    "payRate": "65000.00 USD"
# }

class SendMessage:
    def __init__(self, message: str, message_type: str, recipient: str):
        self.message = message
        self.message_type = message_type
        self.recipient = recipient

    def execute(self):
        url = f'http://localhost:7005/sendMessage'
        headers = {'Accept': 'application/json', 'Content-type': 'application/json'}
        request_body = {"message": "new_message2", "recipient": "testrramos", "message_type": "public"}

        status_code = None
        try:
            raw_response = requests.post(url, json.dumps(request_body), headers=headers)
            status_code = raw_response.status_code
            parsed_response = json.loads(raw_response.text)
            # pay_rate = parsed_response['payRate']
            # pay_rate_parts = pay_rate.split(' ')
            # parsed_response['amount'] = pay_rate_parts[0]
            # parsed_response['currency'] = pay_rate_parts[1]
            response = json.dumps(parsed_response)
        except Exception as ex:
            response = f'{ "error": "{ex}" }'

        return {
            'response': response,
            'status_code': status_code,
            'node_returned_200': True,
            'mimetype': 'application/json'
        }
