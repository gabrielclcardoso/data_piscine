import psycopg
import matplotlib.pyplot as plt

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
                measures = get_measures(cur)
                prices = get_prices(cur)
                avg_basket = get_average_basket_price(cur)
            except Exception as e:
                print(f"{type(e).__name__}: {e}")

    print_measures(measures)
    plot_boxes(prices, avg_basket)


def get_measures(cur: psycopg.Cursor) -> list[float]:
    query = """
    SELECT
        COUNT(*) AS count,
        avg(price) AS mean,
        stddev(price) as std,
        MIN(price) as min,
        percentile_cont(0.25) WITHIN GROUP(ORDER BY price) AS p1,
        percentile_cont(0.5) WITHIN GROUP(ORDER BY price) AS p2,
        percentile_cont(0.75) WITHIN GROUP(ORDER BY price) AS p3,
        MAX(price) as max
    FROM customers
    WHERE event_type = 'purchase';
    """

    print("Calculating measures from the dataset")
    cur.execute(query)
    measures = cur.fetchone()
    return measures


def get_prices(cur: psycopg.Cursor) -> list[float]:
    """Returns all the prices of purchases from the customers table"""

    query = """
    SELECT
        price
    FROM customers
    WHERE event_type = 'purchase';
    """

    print("Calculating average basket price per user")
    cur.execute(query)
    prices = cur.fetchall()
    prices = [i[0] for i in prices]
    return prices


def get_average_basket_price(cur: psycopg.Cursor) -> list[float]:
    """Returns the average basket price per user"""

    query = """
    WITH baskets AS (
        SELECT
            user_id,
            sum(price) AS basket_price
        FROM customers
        WHERE event_type = 'purchase'
        GROUP BY user_id, event_time
    )
    SELECT
        avg(basket_price)
    FROM baskets
    GROUP BY user_id;
    """

    print("Collecting all purchase prices")
    cur.execute(query)
    avg = cur.fetchall()
    avg = [i[0] for i in avg]
    return avg


def print_measures(measures: list[float]) -> None:
    """Prints all the measures collected in a formatted way"""

    labels = ["count", "mean", "std", "min", "25%", "50%", "75%", "max"]

    for label, value in zip(labels, measures):
        print(f"{label:<6} {value:20.6f}")


def plot_boxes(prices: list[float], avg: list[float]) -> None:
    """Plots the different box plots and displays them on screen"""

    plot_price_boxplot(prices)
    plot_avg_boxplot(avg)

    plt.show()


def plot_price_boxplot(prices: list[float]) -> None:
    """Plots 2 boxplots for the prices, with and without outliers"""

    fig1, ax1 = plt.subplots()

    ax1.yaxis.set_visible(False)
    ax1.set_xlabel("price")
    ax1.grid(True)

    bplot = ax1.boxplot(prices, orientation="horizontal", widths=0.9,
                        patch_artist=True, sym="gD", zorder=2)
    bplot["boxes"][0].set_facecolor('springgreen')

    fig2, ax2 = plt.subplots()

    ax2.yaxis.set_visible(False)
    ax2.set_xlabel("price")
    ax2.grid(True)

    bplot = ax2.boxplot(prices, orientation="horizontal", widths=0.9,
                        patch_artist=True, sym="", zorder=2)
    bplot["boxes"][0].set_facecolor('springgreen')


def plot_avg_boxplot(avg: list[float]) -> None:
    """Plots 2 boxplots for the prices, with and without outliers"""

    fig1, ax = plt.subplots()

    ax.yaxis.set_visible(False)
    ax.grid(True)
    # ax.set_xlim(-25, 125)

    bplot = ax.boxplot(avg, orientation="horizontal", widths=0.9,
                       patch_artist=True, sym="gD", zorder=2)
    bplot["boxes"][0].set_facecolor('lightblue')


if __name__ == "__main__":
    main()
