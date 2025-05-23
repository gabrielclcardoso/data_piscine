import psycopg
from sys import stderr


def main():
    db_connection_params = {
        'dbname': 'piscineds',
        'user': 'gcorreia',
        'password': 'mysecretpassword',
        'host': 'localhost'
    }

    with psycopg.connect(**db_connection_params) as conn:
        with conn.cursor() as cur:

            try:
                insert_february(cur)
                table_names = get_table_names(cur)
                create_table(cur, "customers")
                insert_rows(cur, table_names, "customers")
            except Exception as e:
                print(f"{type(e).__name__}: {e}")
                return 1


def insert_february(cur: psycopg.Cursor) -> None:
    """Append additional february data to january table"""

    sql_copy = """
        COPY data_2023_jan
        FROM STDIN
        WITH (
            FORMAT CSV,
            HEADER TRUE
        );
    """

    print("inserting february data")
    with open("data_2023_feb.csv") as f:
        with cur.copy(sql_copy) as copy:
            copy.write(f.read())


def get_table_names(cur: psycopg.Cursor) -> list:
    """Returns a list of all the tables with names that match the data pattern
    """

    query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_name ~ '^data_202[0-9]_[a-z]{3}$';
    """

    print("Fetching table names")
    cur.execute(query)

    return [row[0] for row in cur.fetchall()]


def create_table(cur: psycopg.Cursor, name: str) -> None:
    """Creates the table with name"""

    query = f"""
        CREATE TABLE {name} (
            id SERIAL PRIMARY KEY,
            event_time timestamp with time zone,
            event_type event,
            product_id integer,
            price real,
            user_id bigint,
            user_session char(36)
        );
    """

    print(f"Creating {name} table")
    cur.execute(query)


def insert_rows(cur: psycopg.Cursor, sources: list, dest: str) -> None:
    """Joins all the sources tables into the dest table"""

    rows = "event_time, event_type, product_id, price, user_id, user_session"

    union_string = ""
    for i in sources:
        union_string += f"SELECT {rows} from {i}\nUNION ALL\n"
    union_string = union_string.removesuffix("\nUNION ALL\n")
    union_string += ";"

    query = f"""
        INSERT INTO {dest} ({rows})
        {union_string}
    """

    print(f"Joining {sources} into {dest}")
    cur.execute(query)


if __name__ == "__main__":
    main()
