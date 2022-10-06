import json

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from connector_aws.auths.simpleAuth import SimpleAuth


class ScanDynamoTable:
    """Return all records in a given table.  Potentially very expensive."""

    def __init__(self, access_key: str, secret_key: str, table_name: str):
        """
        :param access_key: AWS Access Key
        :param secret_key: AWS Secret Key
        :param table_name: The name of hte Dynamo DB table to scan
        :return: Json Data structure containing the requested data.
        """
        self.dynamodb = SimpleAuth('dynamodb', access_key, secret_key).get_resource()
        self.table = self.dynamodb.Table(table_name)

    def execute(self, config):
        result = self.table.scan()
        if 'ResponseMetadata' in result:
            del result['ResponseMetadata']
        result_str = json.dumps(result)
        return dict(response=result_str, mimetype='application/json')
