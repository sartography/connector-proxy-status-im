import json

from typing import Any
from typing import Dict

from connector_postgresql.baseCommand import BaseCommand, ConnectionConfig

class DeleteValues(BaseCommand):
    """DeleteValues."""

    def __init__(self,
        database_name: str,
        database_host: str,
        database_port: int,
        database_user: str,
        database_password: str,
        table_name: str,
        schema: Dict[str, Any]
    ):
        """__init__."""
        self.connection_config = ConnectionConfig(
            database_name, 
            database_host, 
            database_port, 
            database_user, 
            database_password)
        self.table_name = table_name
        self.schema = schema

    def execute(self, config, task_data):
        where_clause, values = self.build_where_clause(self.schema)

        # TODO: build properly with SQL().format(Identifier(name))
        # https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries
        sql = f"DELETE FROM {self.table_name} {where_clause};"

        return self.execute_query(sql, self.connection_config, values)

