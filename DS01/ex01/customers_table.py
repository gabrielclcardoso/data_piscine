import psycopg
from pathlib import Path


def main():
    connect_string = """
    host=localhost
    dbname=piscineds
    user=gcorreia
    password=mysecretpassword
    """
    files = get_csv_files("subject/customer")

    try:
        assert len(files) > 0, "No csv files retrieved from subject/customer"
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        exit(1)

    with psycopg.connect(connect_string) as conn:
        with conn.cursor() as cur:
            create_type(cur)
            create_table(cur)
            for f in files:
                copy_content(cur, f)


def get_csv_files(path: str) -> list[Path]:
    """Returns a list of csv files in the given directory"""

    dir = Path(path)
    return list(dir.glob("**/*.csv"))


def create_type(cur: psycopg.Cursor):
    """Creates the type event on the database"""

    events = ('cart', 'view', 'remove_from_cart', 'purchase')

    try:
        cur.execute(f"CREATE TYPE event as ENUM {events};")
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        exit(1)


def create_table(cur: psycopg.Cursor):
    """Creates the table customers on the postgres DB"""

    cur.execute("""
        CREATE TABLE customers (
            event_time timestamp with time zone,
            event_type event,
            product_id integer,
            price real,
            user_id bigint,
            user_session char(36)
        );
    """)


def copy_content(cur: psycopg.Cursor, file: Path):
    """Copies data from the file to customers table"""

    sql_copy = """
        COPY customers
        FROM STDIN
        WITH (
            FORMAT CSV,
            HEADER TRUE
        );
    """

    print(f"Copying content from {file.name}")

    try:
        with file.open() as f:
            with cur.copy(sql_copy) as copy:
                copy.write(f.read())
    except Exception as e:
        print(f"{type(e).__name__} at file {file.name}: {e}")
        exit(1)

    print(f"Copied content from {file.name}")


if __name__ == "__main__":
    main()
