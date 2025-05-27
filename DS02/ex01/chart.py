import psycopg
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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
                customers = get_customers(cur)
                total_sales = get_sales(cur)
                average_spent = get_avg_spend(cur)
            except Exception as e:
                print(f"{type(e).__name__}: {e}")

    plot_customers(customers)
    plot_sales(total_sales)
    plot_average(average_spent)
    plt.show()


def get_customers(cur: psycopg.Cursor) -> list[psycopg.rows.Row]:
    """Returns a list with the amount of customers for each day"""

    query = """
    SELECT
        DATE(event_time) AS date,
        COUNT(DISTINCT user_id) AS count
    FROM customers
    WHERE event_type = 'purchase'
    GROUP BY DATE(event_time)
    ORDER BY DATE(event_time);
    """

    print("Counting customers for each day")
    cur.execute(query)
    counts = cur.fetchall()

    return counts


def get_sales(cur: psycopg.Cursor) -> list[psycopg.rows.Row]:
    """Returns a list with the amount of sales for each month"""

    query = """
    SELECT
        date_trunc('month', event_time) AS month,
        SUM(price) AS price
    FROM customers
    WHERE event_type = 'purchase'
    GROUP BY date_trunc('month', event_time)
    ORDER BY date_trunc('month', event_time);
    """

    print("Counting sales for each month")
    cur.execute(query)
    counts = cur.fetchall()

    return counts


def get_avg_spend(cur: psycopg.Cursor) -> list[psycopg.rows.Row]:
    """Returns a list with the amount of sales for each month"""

    query = """
    WITH daily_sales AS (
        SELECT
            DATE(event_time) AS date,
            SUM(price) AS total_sales,
            COUNT(DISTINCT user_id) AS distinct_users
        FROM customers
        WHERE event_type = 'purchase'
        GROUP BY DATE(event_time)
    )
    SELECT
        date,
        CASE
            WHEN distinct_users > 0 THEN total_sales / distinct_users
            ELSE 0
        END AS average
    FROM daily_sales
    ORDER BY date;
    """

    print("Getting average sales per user for each day")
    cur.execute(query)
    counts = cur.fetchall()

    return counts


def plot_customers(customers: list[psycopg.rows.Row]) -> None:
    """Standard plot with the amount of customers for each day"""

    dates, ammounts = zip(*customers)
    dates = list(dates)
    ammounts = list(ammounts)

    fig, ax = plt.subplots()
    ax.plot(dates, ammounts, zorder=2)
    ax.set_ylabel("Number of customers")

    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    ax.grid(True)
    ax.set_xlim(dates[0], dates[-1])


def plot_sales(sales: list[psycopg.rows.Row]) -> None:
    """bar plot displaying income from sales each month"""

    months, incomes = zip(*sales)
    months = list(months)
    incomes = [(i / 1e6) for i in incomes]

    figure, ax = plt.subplots()
    ax.bar(months, incomes, width=20, zorder=2)
    ax.set_ylabel("total sales in million of ₳")
    ax.set_xlabel("month")

    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    ax.grid(visible=True, axis='y')


def plot_average(average: list[psycopg.rows.Row]) -> None:
    """Standard plot with the amount of customers for each day"""

    dates, avgs = zip(*average)
    dates = list(dates)
    avgs = list(avgs)

    figure, ax = plt.subplots()
    ax.plot(dates, avgs, zorder=2)
    ax.fill_between(dates, avgs, zorder=2)
    ax.set_ylabel("average spend/customers in ₳")

    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    ax.grid(True)
    ax.set_xlim(dates[0], dates[-1])
    ax.set_ylim(bottom=0)


if __name__ == "__main__":
    main()
