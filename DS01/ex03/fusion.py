import psycopg
import datetime


def main():
    db_connection_params = {
        "dbname": "piscineds",
        "user": "gcorreia",
        "password": "mysecretpassword",
        "host": "localhost"
    }

    with psycopg.connect(**db_connection_params) as conn:
        with conn.cursor() as cur:
            try:
                add_columns(cur)
                fill_values(cur)
            except Exception as e:
                print(f"{type(e).__name__}: {e}")
                return 1


def add_columns(cur: psycopg.Cursor) -> None:
    """Create new columns in the customers tables to match the items columns"""

    columns_query = """
    -- Create new rows
    ALTER TABLE customers
        ADD COLUMN category_id category_id_type,
        ADD COLUMN category_code category_code_type,
        ADD COLUMN brand brand_type;
    """

    print("Creating new columns in customers tables")

    start_time = datetime.datetime.now()
    cur.execute(columns_query)
    end_time = datetime.datetime.now()

    print(f"Columns created, elapsed time = {end_time - start_time}")


def fill_values(cur: psycopg.Cursor) -> None:
    """Fills the values of the new columns in customers with the values
    associated with the corresponding item"""

    values_query = """
    --- CTE to create items with no duplicates
    WITH items_nodup AS (
        SELECT
            product_id,
            MAX(category_id) AS category_id,
            MAX(category_code) AS category_code,
            MAX(brand) AS brand
        FROM
           items
        GROUP BY
            product_id
    )

    -- Add values to the customers rows
    UPDATE customers
        SET category_id = items_nodup.category_id,
            category_code = items_nodup.category_code,
            brand = items_nodup.brand
        FROM items_nodup
        WHERE customers.product_id = items_nodup.product_id;
    """

    print("Filling columns with corresponding values")

    start_time = datetime.datetime.now()
    cur.execute(values_query)
    end_time = datetime.datetime.now()

    print(f"Columns filled, elapsed time = {end_time - start_time}")


if __name__ == "__main__":
    main()
