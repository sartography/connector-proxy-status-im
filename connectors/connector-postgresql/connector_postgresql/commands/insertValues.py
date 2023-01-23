import json

from connector_postgresql.baseCommand import BaseCommand

class InsertValues(BaseCommand):
    """InsertValues."""

    def __init__(self, table_name: str, schema: str):
        """__init__."""
        self.table_name = table_name
        self.schema = schema

    def execute(self, config, task_data):
        columns = ",".join(self.schema["columns"])
        placeholders = f"({','.join(['%s'] * len(self.schema['columns']))})"
        value_lists = self.schema["values"]

        # TODO: build properly with SQL().format(Identifier(name))
        # https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries
        sql = f"INSERT INTO {self.table_name} ({columns}) VALUES {placeholders};"

        return self.execute_batch(sql, config, value_lists)
