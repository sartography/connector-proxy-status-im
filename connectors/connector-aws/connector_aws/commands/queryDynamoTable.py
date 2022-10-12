"""QueryDynamoTable."""
import json

from connector_aws.auths.simpleAuth import SimpleAuth  # type: ignore


class QueryDynamoTable:
    """Return all records for a given partition key."""

    def __init__(self, table_name: str, key: str):
        """
        :param table_name: The name of hte Dynamo DB table to add information to.
        :param key: The partition key for what to return.
        :return: Json Data structure containing the requested data.
        """
        self.table_name = table_name
        self.key = key

    def execute(self, config, task_data):
        """Execute."""
        dynamodb = SimpleAuth("dynamodb", config).get_resource()
        table = dynamodb.Table(self.table_name)
        result = table.get_item(Key={"primaryKeyName": self.key})
        if "ResponseMetadata" in result:
            del result["ResponseMetadata"]
        result_str = json.dumps(result)
        return dict(response=result_str, mimetype="application/json")
