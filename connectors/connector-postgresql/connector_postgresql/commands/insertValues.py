import json
import psycopg2

class InsertValues:
    """InsertValues."""

    def __init__(self, table_name: str, schema: str):
        """__init__."""
        self.table_name = table_name
        self.schema = json.loads(schema)

    def execute(self, config, task_data):

        columns = self._column_definitions(self.schema)
        (placeholders, values) = self._insert_values(self.schema)

        # TODO: build properly with SQL().format(Identifier(name))
        # https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries
        sql = f"INSERT INTO {self.table_name} ({columns}) VALUES {placeholders};"

        print(sql)

        with psycopg2.connect(self._get_db_connection_str(config)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, values)
                conn.commit

        return {"response": f'{{"result": "created table {self.table_name}"}}', "status": 200, "mimetype": "application/json"}

    def _get_db_connection_str(self, config):
        database = config["POSTGRESQL_DB_NAME"]
        username = config["POSTGRESQL_USER_NAME"]
        password = config["POSTGRESQL_PASSWORD"]
        
        return f"dbname={database} user={username} password={password}"

    def _column_definitions(self, schema):
        return ",".join(schema["columns"])

    def _insert_values(self, schema):
        def to_placeholders(values_list):
            return f"({','.join(['%s'] * len(values_list))})"
        value_lists = schema["values"]
        placeholders = ",".join(map(to_placeholders, value_lists))
        values = [v for value_list in value_lists for v in value_list]

        return (placeholders, values)
