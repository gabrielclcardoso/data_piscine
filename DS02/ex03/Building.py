import psycopg
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

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
                data = get_data(cur)
            except Exception as e:
                print(f"{type(e).__name__}: {e}")

    plot_histograms(data)


def get_data(cur: psycopg.Cursor) -> list[psycopg.rows.Row]:
    """Returns the ammount of times each user purchased from the website"""

    query = """
    SELECT
        COUNT(*) AS number_of_orders,
        SUM(price) AS total_spent
    FROM customers
    WHERE event_type = 'purchase'
    GROUP BY user_id, event_time;
    """

    print("Collecting all purchase prices")
    cur.execute(query)
    data = cur.fetchall()
    return data


def plot_histograms(data: list[psycopg.rows.Row]) -> None:
    """Plots 2 barplots to display the ammount of users in each frequency
    interval and the ammount of users in each spending interval"""

    frequencies, total_spent = zip(*data)
    fig, axs = plt.subplots(1, 2)

    plot_frequency_hist(frequencies, axs[0])
    plot_spent_hist(total_spent, axs[1])

    plt.show()


def plot_frequency_hist(frequencies: list[float], ax) -> None:
    """Plots a histogram for the frequencies"""

    ax.set_xlabel("frequency")
    ax.set_ylabel("customers")
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1e4))
    ax.grid(True)

    ax.hist(frequencies, bins=[1, 8, 15, 23, 31, 38], rwidth=0.97, zorder=2)


def plot_spent_hist(total_spent: list[float], ax) -> None:
    """Plots a histogram for the total ammount spent"""

    ax.set_xlabel("monetary value in ₳")
    ax.set_ylabel("customers")
    ax.xaxis.set_major_locator(ticker.MultipleLocator(50))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(5e3))
    ax.grid(True)

    ax.hist(total_spent, bins=[-25, 25, 75, 125, 175, 225], rwidth=0.97,
            zorder=2)


if __name__ == "__main__":
    main()
