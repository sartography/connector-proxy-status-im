import json

from connector_postgresql.baseCommand import BaseCommand

class CreateTable(BaseCommand):
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

        response, status = self.execute_query(sql, config)

        return {"response": response, "status": status, "mimetype": "application/json"}

    def _column_definitions(self, schema):
        def column_defintion(column):
            return f"{column} VARCHAR"

        column_names = schema["columns"]
        column_definitions = map(column_defintion, column_names)
        
        return ",".join(column_definitions)
