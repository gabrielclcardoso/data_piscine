import psycopg
from pathlib import Path


def main():
    connect_string = """
    host=localhost
    dbname=piscineds
    user=gcorreia
    """
    files = get_csv_files("subject/customer")

    with psycopg.connect(connect_string) as conn:
        with conn.cursor() as cur:
            try:
                create_type(cur)
            except Exception as e:
                print(f"Error: {e}")
                conn.rollback()
            for f in files:
                try:
                    create_table(cur, f)
                    copy_content(cur, f)
                except Exception as e:
                    print(f"Error at file {f.name}: {e}")
                    conn.rollback()


def create_type(cur: psycopg.Cursor):
    """Creates the TYPE event on the database"""
    events = ('cart', 'view', 'remove_from_cart', 'purchase')

    cur.execute(f"CREATE TYPE event as ENUM {events};")


def get_csv_files(path: str) -> list[Path]:
    """Returns a list of csv files in the given directory"""

    dir = Path(path)
    return list(dir.glob("**/*.csv"))


def create_table(cur: psycopg.Cursor, file: Path):
    """Creates the table acording to the file name"""

    cur.execute(f"""
        CREATE TABLE {file.name[-4]} (
            event_time timestamp with time zone,
            event_type event,
            product_id integer,
            price real,
            user_id bigint,
            user_session char(36)
        );
    """)


def copy_content(cur: psycopg.Cursor, file: Path):
    """Copies data from the file to it's respective table"""

    sql_copy = f"""
        COPY {file.name[-4]}
        FROM STDIN
        WITH (
            FORMAT CSV,
            HEADER TRUE
        );
    """

    with file.open() as f:
        with cur.copy(sql_copy) as copy:
            copy.write(f.read())


if __name__ == "__main__":
    main()
