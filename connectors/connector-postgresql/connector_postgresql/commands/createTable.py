import json
import psycopg2

class CreateTable:
    """CreateTable."""

    def __init__(self, table_name: str, schema: str):
        """__init__."""
        self.table_name = table_name
        self.schema = json.loads(schema)

    def execute(self, config, task_data):

        columns = self._column_definitions(self.schema)
        # TODO: build properly with SQL().format(Identifier(name))
        # https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries
        sql = f"CREATE TABLE {self.table_name} ({columns});"

        with psycopg2.connect(self._get_db_connection_str(config)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                conn.commit

        return {"response": f'{{"result": "created table {self.table_name}"}}', "status": 200, "mimetype": "application/json"}

    def _get_db_connection_str(self, config):
        database = config["POSTGRESQL_DB_NAME"]
        username = config["POSTGRESQL_USER_NAME"]
        password = config["POSTGRESQL_PASSWORD"]
        
        return f"dbname={database} user={username} password={password}"

    def _column_definitions(self, schema):
        def column_defintion(column):
            return f"{column} VARCHAR"

        column_names = schema["columns"]
        column_definitions = map(column_defintion, column_names)
        
        return ",".join(column_definitions)
