# import psycopg
from pathlib import Path


def main():
    iterate_directory("subject")
    # with psycopg.connect("host=localhost dbname=piscineds user=gcorreia " +
    #                      "password=mysecretpassword") as conn:
    #     with conn.cursor() as cur:
    #         create_table(conn, cur)
    #         copy_from_csv(conn, cur)


def iterate_directory(path: str) -> None:
    dir = Path(path)
    csv_files = list(dir.glob("**/*.csv"))
    for f in csv_files:
        print(f.name[:-4])

# def create_table(conn, cur):
#     """Creates the table data_2022_oct if it doesn't exist"""
#
#     events = ('cart', 'view', 'remove_from_cart', 'purchase')
#
#     try:
#         cur.execute(f"CREATE TYPE event as ENUM {events};")
#     except psycopg.Error as e:
#         print(f"Error: {e}")
#         conn.rollback()
#
#     try:
#         cur.execute("""
#             CREATE TABLE data_2022_oct (
#                 event_time timestamp with time zone,
#                 event_type event,
#                 product_id integer,
#                 price real,
#                 user_id bigint,
#                 user_session char(36)
#             );
#         """)
#     except psycopg.Error as e:
#         print(f"Error: {e}")
#         conn.rollback()
#
#
# def copy_from_csv(conn, cur):
#     """Copies data in the subject/customer/data_2022_oct.csv file"""
#
#     sql_copy = """
#         COPY data_2022_oct
#         FROM STDIN
#         WITH (
#             FORMAT CSV,
#             HEADER TRUE
#         );
#     """
#
#     try:
#         with open("subject/customer/data_2022_oct.csv") as f:
#             with cur.copy(sql_copy) as copy:
#                 copy.write(f.read())
#     except Exception as e:
#         print(f"Error: {e}")


if __name__ == "__main__":
    main()
