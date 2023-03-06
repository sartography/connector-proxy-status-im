import json

from connector_postgresql.baseCommand import BaseCommand, ConnectionConfig

class DropTable(BaseCommand):
    """DropTable."""

    def __init__(self,
        database_connection_str: str,
        table_name: str
    ):
        """__init__."""
        self.database_connection_str = database_connection_str
        self.table_name = table_name

    def execute(self, config, task_data):

        # TODO: build properly with SQL().format(Identifier(name))
        # https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries
        sql = f"DROP TABLE IF EXISTS {self.table_name};"

        return self.execute_query(sql, self.database_connection_str)

