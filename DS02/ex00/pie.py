import psycopg
import matplotlib.pyplot as plt

DB_CONN_PARAMS = {
    "dbname": "piscineds",
    "user": "gcorreia",
    "password": "mysecretpassword",
    "host": "localhost"
}

LABELS = ["view", "cart", "remove_from_cart", "purchase"]


def main():
    with psycopg.connect(**DB_CONN_PARAMS) as conn:
        with conn.cursor() as cur:
            try:
                counts = get_counts(cur, LABELS, "event_type")
            except Exception as e:
                print(f"{type(e).__name__}: {e}")

    plot_pie(LABELS, counts)


def get_counts(cur: psycopg.Cursor, labels: list[str], col: str) -> list[int]:
    """Return the count for each label listed in labels present in the column
    col from the customers table"""

    query = "SELECT"
    for label in labels:
        query += f"\nCOUNT(CASE WHEN {col} = '{label}' THEN 1 END) AS {label},"
    query = query[:-1]
    query += "\nFROM customers;"

    print(f"Counting instances of {labels} in column {col}")
    cur.execute(query)
    counts = cur.fetchone()

    return list(counts)


def plot_pie(labels: list[str], sizes: list[int]) -> None:
    """Plots a pie chart with the given label and sizes"""

    explode = [0.005 for i in labels]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", explode=explode)
    plt.show()


if __name__ == "__main__":
    main()
