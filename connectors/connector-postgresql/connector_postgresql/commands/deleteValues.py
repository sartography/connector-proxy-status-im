import json

from connector_postgresql.baseCommand import BaseCommand

class DeleteValues(BaseCommand):
    """DeleteValues."""

    def __init__(self, table_name: str, schema: str):
        """__init__."""
        self.table_name = table_name
        self.schema = schema

    def execute(self, config, task_data):
        where_clause, values = self.build_where_clause(self.schema)

        # TODO: build properly with SQL().format(Identifier(name))
        # https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries
        sql = f"DELETE FROM {self.table_name} {where_clause};"

        return self.execute_query(sql, config, values)

