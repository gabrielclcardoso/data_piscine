import csv
from sys import stderr

import psycopg


def main():
    connect_string = """
    host=localhost
    dbname=piscineds
    user=gcorreia
    password=mysecretpassword
    """

    with open("subject/item/item.csv") as f:
        sets = get_sets(f)

        with psycopg.connect(connect_string) as conn:
            with conn.cursor() as cur:
                create_types(cur, sets)
                create_table(cur)
                f.seek(0)
                copy_content(cur, f)


def get_sets(file):
    """Reads the items.csv file and returns a dictonary with 2 sets, one
    representing the options for category code and one representing the options
    for brand
    """

    table = csv.DictReader(file)
    sets = {'category_code': set(), 'brand': set()}

    try:
        for row in table:
            sets['category_code'].add(row['category_code'])
            sets['brand'].add(row['brand'])
    except Exception as e:
        print("Error: make sure the csv file is correct",
              file=stderr)
        print(f"{type(e).__name__}: {e}", file=stderr)
        exit(1)

    return sets


def create_types(cur: psycopg.Cursor, sets: dict):
    """Creates the 3 types needed for the item database"""

    sql = "CREATE DOMAIN category_id_type AS TEXT CHECK (VALUE ~ '^[0-9]+$')"

    try:
        for key, value in sets.items():
            cur.execute(f"CREATE TYPE {key}_type as ENUM {tuple(value)};")
            print(f"{key} type created")
        cur.execute(sql)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        exit(1)


def create_table(cur: psycopg.Cursor):
    """Creates the items table """

    try:
        cur.execute("""
            CREATE TABLE items (
                product_id integer,
                category_id category_id_type,
                category_code category_code_type,
                brand brand_type
            );
        """)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        exit(1)

    print("items table created")


def copy_content(cur: psycopg.Cursor, file):
    """Copies data from the file to it's respective table"""

    sql_copy = """
        COPY items
        FROM STDIN
        WITH (
            FORMAT CSV,
            HEADER TRUE
        );
    """
    print(f"Copying content from {file.name}")

    try:
        with cur.copy(sql_copy) as copy:
            copy.write(file.read())
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        exit(1)

    print(f"Copied content from {file.name}")


if __name__ == "__main__":
    main()
