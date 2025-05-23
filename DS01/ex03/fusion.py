import psycopg

QUERY = """
-- Create new rows
ALTER TABLE customers
    ADD COLUMN category_id category_id_type,
    ADD COLUMN category_code category_code_type,
    ADD COLUMN brand brand_type;

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
                cur.execute(QUERY)
            except Exception as e:
                print(f"{type(e).__name__}: {e}")
                return 1


if __name__ == "__main__":
    main()
