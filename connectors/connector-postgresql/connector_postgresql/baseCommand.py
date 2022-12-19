import json
import psycopg2

class BaseCommand:
    """BaseCommand."""

    def _execute(self, sql, config, handler):
        try:
            conn = psycopg2.connect(self._get_db_connection_str(config))
            with conn.cursor() as cursor:
                response = handler(conn, cursor)
                if response is None:
                    if cursor.rowcount >= 0:
                        response = f'{{"result": "{cursor.rowcount} rows affected"}}'
                    else:
                        response = '{"result": "ok"}'
            status = 200
        except Exception as e:
            raise e
            status = 500
            # TODO: better error message, e has no reason and str repr contains quotes
            response = '{"error": "Error executing sql statement"}'
        finally:
            conn.close()

        return {"response": response, "status": status, "mimetype": "application/json"}

    def execute_query(self, sql, config):
        def handler(conn, cursor):
            cursor.execute(sql)
            conn.commit()

        return self._execute(sql, config, handler)

    def execute_batch(self, sql, config, vars_list):
        def handler(conn, cursor):
            cursor.executemany(sql, vars_list)
            # TODO: look more into getting this to work instead
            # psycopg2.extras.execute_batch(cursor, sql, vars_list)
            # https://www.psycopg.org/docs/extras.html#fast-exec
            conn.commit()

        return self._execute(sql, config, handler)

    def fetchall(self, sql, config):
        def prep_results(results):
            return list(map(list, results))
        def handler(conn, cursor):
            cursor.execute(sql)
            return json.dumps(prep_results(cursor.fetchall()))

        return self._execute(sql, config, handler)

    def _get_db_connection_str(self, config):
        database = config["POSTGRESQL_DB_NAME"]
        username = config["POSTGRESQL_USER_NAME"]
        password = config["POSTGRESQL_PASSWORD"]
        
        return f"dbname={database} user={username} password={password}"
