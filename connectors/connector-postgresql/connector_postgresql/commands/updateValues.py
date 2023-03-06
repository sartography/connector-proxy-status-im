import json

from typing import Any
from typing import Dict

from connector_postgresql.baseCommand import BaseCommand, ConnectionConfig

class UpdateValues(BaseCommand):
    """UpdateValues."""

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
        set_clause, values = self._build_set_clause(self.schema)
        where_clause, where_values = self.build_where_clause(self.schema)

        if where_values is not None:
            values += where_values

        # TODO: build properly with SQL().format(Identifier(name))
        # https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries
        sql = f"UPDATE {self.table_name} {set_clause} {where_clause};"

        return self.execute_query(sql, self.database_connection_str, values)

    def _build_set_clause(self, schema):
        columns_to_values = schema["set"]
        columns, values = zip(*columns_to_values.items())
        set_columns = ", ".join(map(lambda c: f"{c} = %s", columns))

        return f"SET {set_columns}", values

