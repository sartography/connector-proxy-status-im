import json

from typing import Any
from typing import Dict

from psycopg2.extras import Json
from psycopg2.extensions import register_adapter

register_adapter(dict, Json)

from connector_postgresql.baseCommand import BaseCommand, ConnectionConfig

class DoSQL(BaseCommand):
    """DoSQL."""

    def __init__(self,
        database_connection_str: str,
        schema: Dict[str, Any]
    ):
        """__init__."""
        self.database_connection_str = database_connection_str
        self.schema = schema

    def execute(self, config, task_data):

        sql = self.schema["sql"]
        values = self.schema.get("values", [])
        fetch_results = self.schema.get("fetch_results", False)

        if fetch_results:
            return self.fetchall(sql, self.database_connection_str, values)

        return self.execute_query(sql, self.database_connection_str, values)
