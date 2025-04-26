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
            table_names = get_table_names(cur)
            if not table_names:
                return 1
            print(table_names)


def get_table_names(cur: psycopg.Cursor) -> list:
    """Returns a list of all the tables with names that match the data pattern
    """

    query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_name ~ '^data_202[0-9]_[a-z]{3}$';
    """

    try:
        cur.execute(query)
    except Exception as e:
        print(f"{type(e).__name__}: {e}", file=stderr)
        return None

    return [row[0] for row in cur.fetchall()]


if __name__ == "__main__":
    main()
