import csv
from sys import stderr

import psycopg

def main():

    try:
        f = open("subject/item/item.csv")
    except Exception as e:
        print(f"{type(e).__name__}: {e}", file=stderr)
        exit(1)
def main():
    connect_string = """
    host=localhost
    dbname=piscineds
    user=gcorreia
    password=mysecretpassword
    """

    with open("subject/item/item.csv") as f:
        try:
            sets = get_sets(f)
            print(sets)
        except Exception as e:
            print("Error: make sure the csv file is correct",
                  file=stderr)
            print(f"{type(e).__name__}: {e}", file=stderr)
            exit(1)

        with psycopg.connect(connect_string) as conn:
            with conn.cursor() as cur:
                try:
                    create_types(cur, sets)
                except Exception as e:
                    print(f"{type(e).__name__}: {e}")
                    conn.rollback()

def get_sets(file):
    """Reads the items.csv file and returns a dictonary with 2 sets, one
    representing the options for category code and one representing the options
    for brand
    """

    table = csv.DictReader(file)
    sets = {'category_code': set(), 'brand': set()}

    for row in table:
        sets['category_code'].add(row['category_code'])
        sets['brand'].add(row['brand'])

    return sets


def create_types(cur: psycopg.Cursor, sets: dict):
    """Creates the 3 types needed for the item database"""

    for key, value in sets.items():
        cur.execute(f"CREATE TYPE {key} as ENUM {tuple(value)};")
        print(f"{key} type created")

    sql = "CREATE DOMAIN category_id AS TEXT CHECK (VALUE ~ '^[0-9]+$')"
    cur.execute(sql)


if __name__ == "__main__":
    main()
