import psycopg2

class BaseCommand:
    """BaseCommand."""
    def perform_query(self, sql, config):
        status = 200
        result = '{"result": "ok"}'

        try:
            conn = psycopg2.connect(self._get_db_connection_str(config))
            with conn.cursor() as cursor:
                cursor.execute(sql)
                conn.commit()
                if cursor.rowcount >= 0:
                    result = f'{{"result": "{cursor.rowcount} affected"}}'
        except Exception as e:
            status = 500
            # TODO: better error message, e has no reason and str repr contains quotes
            result = '{"error": "Error executing sql statement"}'
        finally:
            conn.close()

        return (result, status)

    def _get_db_connection_str(self, config):
        database = config["POSTGRESQL_DB_NAME"]
        username = config["POSTGRESQL_USER_NAME"]
        password = config["POSTGRESQL_PASSWORD"]
        
        return f"dbname={database} user={username} password={password}"
