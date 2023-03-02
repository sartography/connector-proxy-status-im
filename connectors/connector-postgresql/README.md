# Postgres Connector

## Commands

### Create Table

Creates a table with the provided column names and their [types](https://www.postgresql.org/docs/current/datatype.html).

The schema parameter expects a key called `column_definitions`. The value associated with this key is a list of dictionaries, each containing the `name` and `type` of a column.

As an example, to create a table like:

```
dev=# \d states;
                       Table "public.states"
 Column  |          Type          | Collation | Nullable | Default 
---------+------------------------+-----------+----------+---------
 country | character varying(255) |           |          | 
 state   | character varying(13)  |           |          | 
 abbrev  | character(2)           |           |          | 
 somenum | integer                |           |          | 

```

The schema passed to the connector would be:

```
{"column_definitions": [
    {
        "name": "country",
        "type": "varchar(255)",
    },
    {
        "name": "state",
        "type": "varchar(13)",
    },
    {
        "name": "abbrev",
        "type": "char(2)",
    },
    {
        "name": "somenum",
        "type": "int",
    }
]}
```
