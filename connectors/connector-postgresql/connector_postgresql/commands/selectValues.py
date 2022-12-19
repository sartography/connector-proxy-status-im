import json
import psycopg2

class SelectValues:
    """SelectValues."""

    def __init__(self, table_name: str, schema: str):
        """__init__."""
        self.table_name = table_name
        self.schema = json.loads(schema)

    def execute(self, config, task_data):

        columns = self._column_definitions(self.schema)

        # TODO: build properly with SQL().format(Identifier(name))
        # https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries
        # TODO: where
        sql = f"SELECT {columns} FROM {self.table_name};"

        with psycopg2.connect(self._get_db_connection_str(config)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                result = json.dumps(self._prep_results(cursor.fetchall()))

        return {"response": f'{{"result": {result}}}', "status": 200, "mimetype": "application/json"}

    def _get_db_connection_str(self, config):
        database = config["POSTGRESQL_DB_NAME"]
        username = config["POSTGRESQL_USER_NAME"]
        password = config["POSTGRESQL_PASSWORD"]
        
        return f"dbname={database} user={username} password={password}"

    def _column_definitions(self, schema):
        return ",".join(schema["columns"])

    def _prep_results(self, results):
        return list(map(list, results))
