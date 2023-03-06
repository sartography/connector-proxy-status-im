import json

from typing import Any
from typing import Dict

from connector_postgresql.baseCommand import BaseCommand, ConnectionConfig

class CreateTable(BaseCommand):
    """CreateTable."""

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

        columns = self._column_definitions(self.schema)
        # TODO: build properly with SQL().format(Identifier(name))
        # https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries
        sql = f"CREATE TABLE IF NOT EXISTS {self.table_name} ({columns});"

        return self.execute_query(sql, self.database_connection_str)

    def _column_definitions(self, schema):
        def column_defintion(column):
            return f"{column['name']} {column['type']}"

        column_definitions = map(column_defintion, schema["column_definitions"])
        
        return ",".join(column_definitions)
