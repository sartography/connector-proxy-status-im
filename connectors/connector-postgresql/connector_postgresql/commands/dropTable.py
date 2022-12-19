import json
import psycopg2

class DropTable:
    """DropTable."""

    def __init__(self, table_name: str):
        """__init__."""
        self.table_name = table_name

    def execute(self, config, task_data):

        # TODO: build properly with SQL().format(Identifier(name))
        # https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries
        sql = f"DROP TABLE {self.table_name};"

        try:
            with psycopg2.connect(self._get_db_connection_str(config)) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    conn.commit
            status = 200
            response = f'{{"result": "dropped table {self.table_name}"}}'
        except Exception as e:
            status = 500
            response = f'{{"error": "unable to drop table {self.table_name}"}}'

        return {"response": response, "status": status, "mimetype": "application/json"}

    def _get_db_connection_str(self, config):
        database = config["POSTGRESQL_DB_NAME"]
        username = config["POSTGRESQL_USER_NAME"]
        password = config["POSTGRESQL_PASSWORD"]
        
        return f"dbname={database} user={username} password={password}"
