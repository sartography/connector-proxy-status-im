import json

from connector_postgresql.baseCommand import BaseCommand

class DropTable(BaseCommand):
    """DropTable."""

    def __init__(self, table_name: str):
        """__init__."""
        self.table_name = table_name

    def execute(self, config, task_data):

        # TODO: build properly with SQL().format(Identifier(name))
        # https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries
        sql = f"DROP TABLE {self.table_name};"

        return self.execute_query(sql, config)

