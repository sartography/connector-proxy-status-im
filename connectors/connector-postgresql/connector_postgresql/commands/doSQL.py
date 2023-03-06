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
        database_name: str,
        database_host: str,
        database_port: int,
        database_user: str,
        database_password: str,
        schema: Dict[str, Any]
    ):
        """__init__."""
        self.connection_config = ConnectionConfig(
            database_name, 
            database_host, 
            database_port, 
            database_user, 
            database_password)
        self.schema = schema

    def execute(self, config, task_data):

        sql = self.schema["sql"]
        values = self.schema.get("values", [])
        fetch_results = self.schema.get("fetch_results", False)

        if fetch_results:
            return self.fetchall(sql, self.connection_config, values)

        return self.execute_query(sql, self.connection_config, values)
