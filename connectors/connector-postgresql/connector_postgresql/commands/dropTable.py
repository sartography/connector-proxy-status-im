import json

from connector_postgresql.baseCommand import BaseCommand, ConnectionConfig

class DropTable(BaseCommand):
    """DropTable."""

    def __init__(self,
        database_name: str,
        database_host: str,
        database_port: int,
        database_user: str,
        database_password: str,
        table_name: str
    ):
        """__init__."""
        self.connection_config = ConnectionConfig(
            database_name, 
            database_host, 
            database_port, 
            database_user, 
            database_password)
        self.table_name = table_name

    def execute(self, config, task_data):

        # TODO: build properly with SQL().format(Identifier(name))
        # https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries
        sql = f"DROP TABLE {self.table_name};"

        return self.execute_query(sql, self.connection_config)

