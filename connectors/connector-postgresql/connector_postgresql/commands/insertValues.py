import json

from typing import Any
from typing import Dict

from connector_postgresql.baseCommand import BaseCommand, ConnectionConfig

class InsertValues(BaseCommand):
    """InsertValues."""

    def __init__(self,
        database_connection_str: str,
        table_name: str,
        schema: Dict[str, Any]
    ):
        """__init__."""
        self.database_connection_str = database_connection_str
        self.table_name = table_name
        self.schema = schema

    def execute(self, config, task_data):
        columns = ",".join(self.schema["columns"])
        placeholders = f"({','.join(['%s'] * len(self.schema['columns']))})"
        value_lists = self.schema["values"]

        # TODO: build properly with SQL().format(Identifier(name))
        # https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries
        sql = f"INSERT INTO {self.table_name} ({columns}) VALUES {placeholders};"

        return self.execute_batch(sql, self.database_connection_str, value_lists)
