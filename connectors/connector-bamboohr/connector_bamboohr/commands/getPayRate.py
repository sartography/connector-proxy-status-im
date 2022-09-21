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

class GetPayRate:
    def __init__(self, api_key: str, subdomain: str, employee_id: str):
        self.api_key = api_key
        self.subdomain = subdomain
        self.employee_id = employee_id

    def execute(self):
        url = f'https://api.bamboohr.com/api/gateway.php/{self.subdomain}/v1/employees/{self.employee_id}'
        headers = {'Accept': 'application/json'}
        params = {'fields': 'payRate', 'onlyCurrent': 'true'}
        auth = (self.api_key, 'x')

        try:
            raw_response = requests.get(url, params, headers=headers, auth=auth)
            parsed_response = json.loads(raw_response.text)
            pay_rate = parsed_response['payRate']
            pay_rate_parts = pay_rate.split(' ')
            parsed_response['amount'] = pay_rate_parts[0]
            parsed_response['currency'] = pay_rate_parts[1]
            response = json.dumps(parsed_response)
        except:
            response = '{ "error": "Invalid Employee ID" }'

        return {
            'response': response,
            'status': raw_response.status_code,
            'mimetype': 'application/json'
        }
