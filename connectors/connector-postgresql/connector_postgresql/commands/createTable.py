import psycopg2

class CreateTable:
    """CreateTable."""

    def __init__(self, schema: dict[str, any]):
        """__init__."""
        self.schema = schema

    def execute(self, config, task_data):
        pass
