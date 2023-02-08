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
            status = 500
            # TODO: better error message, e has no reason and str repr contains quotes
            response = '{"error": "Error executing sql statement"}'
        finally:
            conn.close()

        return {"response": response, "status": status, "mimetype": "application/json"}

    def execute_query(self, sql, config, values=None):
        def handler(conn, cursor):
            cursor.execute(sql, values)
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

    def fetchall(self, sql, config, values):
        def prep_results(results):
            return list(map(list, results))
        def handler(conn, cursor):
            cursor.execute(sql, values)
            return json.dumps(prep_results(cursor.fetchall()))

        return self._execute(sql, config, handler)

    def build_where_clause(self, schema):
        where_configs = schema.get("where", [])
        if len(where_configs) == 0:
            return "", None
        
        operators = {"=", "!=", "<", ">"}
        
        def build_where_part(where_config):
            column, operator, value = where_config
            if operator not in operators:
                raise Exception(f"Unsupported operator '{operator}' in where clause")
            return (f"{column} {operator} {value}")
        
        where_parts = map(build_where_part, where_configs)
        columns, values = zip(*where_parts)
        
        return f"WHERE {' AND '.join(columns)}", values

    def _get_db_connection_str(self, config):
        host = config["POSTGRESQL_HOST"]
        port = config["POSTGRESQL_PORT"]
        database = config["POSTGRESQL_DB_NAME"]
        username = config["POSTGRESQL_USER_NAME"]
        password = config["POSTGRESQL_PASSWORD"]
        
        return f"dbname={database} user={username} password={password} host={host} port={port}"
