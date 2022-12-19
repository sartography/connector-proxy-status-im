import psycopg2

class BaseCommand:
    """BaseCommand."""

    def execute_query(self, sql, config):
        status = 200
        result = '{"result": "ok"}'

        try:
            conn = psycopg2.connect(self._get_db_connection_str(config))
            with conn.cursor() as cursor:
                cursor.execute(sql)
                conn.commit()
                if cursor.rowcount >= 0:
                    result = f'{{"result": "{cursor.rowcount} rows affected"}}'
        except Exception as e:
            status = 500
            # TODO: better error message, e has no reason and str repr contains quotes
            result = '{"error": "Error executing sql statement"}'
        finally:
            conn.close()

        return (result, status)

    # TODO: refactor with execute_query
    def execute_batch(self, sql, config, vars_list):
        status = 200
        response = '{"result": "ok"}'

        try:
            conn = psycopg2.connect(self._get_db_connection_str(config))
            with conn.cursor() as cursor:
                cursor.executemany(sql, vars_list)
                # TODO: look more into getting this to work instead
                # psycopg2.extras.execute_batch(cursor, sql, vars_list)
                conn.commit()
                if cursor.rowcount >= 0:
                    response = f'{{"result": "{cursor.rowcount} rows affected"}}'
        except Exception as e:
            raise e
            status = 500
            # TODO: better error message, e has no reason and str repr contains quotes
            response = '{"error": "Error executing sql statement"}'
        finally:
            conn.close()

        return (response, status)

    def _get_db_connection_str(self, config):
        database = config["POSTGRESQL_DB_NAME"]
        username = config["POSTGRESQL_USER_NAME"]
        password = config["POSTGRESQL_PASSWORD"]
        
        return f"dbname={database} user={username} password={password}"
