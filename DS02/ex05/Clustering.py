import psycopg
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

DB_CONN_PARAMS = {
    "dbname": "piscineds",
    "user": "gcorreia",
    "password": "mysecretpassword",
    "host": "localhost"
}


def main():
    with psycopg.connect(**DB_CONN_PARAMS) as conn:
        with conn.cursor() as cur:
            try:
                loyalty_data = get_data(cur)
            except Exception as e:
                print(f"{type(e).__name__}: {e}")

    transformed_data = transform_data(loyalty_data)
    plot_histogram(transformed_data)


def get_data(cur: psycopg.Cursor) -> list[psycopg.rows.Row]:
    """Returns the ammount of times each user purchased from the website"""

    query = """
    WITH baskets AS (
        SELECT
            user_id,
            sum(price) AS basket_price,
            EXTRACT(EPOCH FROM event_time) AS unix
        FROM customers
        WHERE event_type = 'purchase'
        GROUP BY user_id, event_time
    )
    SELECT
        COUNT(*) AS frequency,
        MAX(unix) AS last_purchase,
        avg(basket_price)
    FROM baskets
    GROUP BY user_id
    ORDER BY frequency;
    """

    print("Collecting loyalty data")
    cur.execute(query)
    data = cur.fetchall()
    return np.array(data)


def transform_data(data: np.ndarray) -> np.ndarray:
    """Removes frequency outlier, transforms the frequency column to it's log
    value and then MinMaxes the frequency and last purchase columns"""

    data = data[data[:, 0] <= max(data[:, 0] * 0.5)]
    data[:, 0] = np.log(data[:, 0].astype(float))
    data[:, 0:2] = MinMaxScaler().fit_transform(data[:, 0:2])
    return data


def plot_histogram(data: np.ndarray) -> None:

    fig, axs = plt.subplots(1, 2)

    axs[0].set_title("Frequency distribution")
    axs[0].grid(True)
    axs[0].hist(data[:, 0], rwidth=0.97, zorder=2)

    axs[1].set_title("last purchase distribution")
    axs[1].grid(True)
    axs[1].hist(data[:, 1], rwidth=0.97, zorder=2)
    plt.show()


if __name__ == "__main__":
    main()
