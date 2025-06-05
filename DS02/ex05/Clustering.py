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

    transformed_data, scaler = transform_data(loyalty_data)
    labeled_data = label_data(transformed_data)
    rescaled_data = rescale_data(labeled_data, scaler)
    plot_visualizations(rescaled_data)


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
    """Removes outliers and then MinMaxes the columns"""

    print("Cleaning and scaling data")
    # Remove outliers in frequency
    data = data[data[:, 0] <= 40]

    # Remove outliers in avg basket price
    mask = (data[:, 2] > 0) & (data[:, 2] < 400)
    data = data[mask]

    # Betters distribution for frequency and avg basket price
    data[:, [0, 2]] = np.log(data[:, [0, 2]].astype(float))

    # Scales data
    scaler = MinMaxScaler()
    data = scaler.fit_transform(data)

    return data, scaler


def label_data(data: np.ndarray) -> np.ndarray:
    """Groups the clients into N_K groups"""

    N_K = 5  # Established through elbow method

    print("Clustering data")
    kmeans = KMeans(n_clusters=N_K, random_state=42).fit(data)
    data = np.column_stack((data, kmeans.labels_))
    return data


def rescale_data(data: np.ndarray, scaler: MinMaxScaler) -> np.ndarray:
    """Removes outliers and then MinMaxes the columns"""

    print("Rescaling data")
    # Inverses MinMaxing
    data[:, 0:3] = scaler.inverse_transform(data[:, 0:3])

    # Inverses log conversion
    data[:, [0, 2]] = np.exp(data[:, [0, 2]])

    return data


def plot_visualizations(data: np.ndarray):
    """Plots the group visualizations"""

    print("Plotting data")
    # scatter_plot(data)
    bar_plot(data)


def scatter_plot(data: np.ndarray):
    """Plots 3 scatter plots to see feature correlation"""

    fig, axs = plt.subplots(1, 3)

    dates = data[:, 1].astype('datetime64[s]')
    ref_date = np.datetime64('2023-03-01')
    month_diff = ((ref_date - dates) / np.timedelta64(1, 'D')).astype("float")

    scatter = axs[0].scatter(month_diff, data[:, 0], c=data[:, 3], alpha=0.5)
    axs[0].set_xlabel("Days since last purchase")
    axs[0].set_ylabel("Number of purchases")
    legend1 = axs[0].legend(*scatter.legend_elements(),
                            loc="upper right", title="Classes")
    axs[0].add_artist(legend1)

    axs[1].scatter(data[:, 2], data[:, 0], c=data[:, 3], alpha=0.5)
    axs[1].set_xlabel("Average basket price")
    axs[1].set_ylabel("Number of purchases")

    axs[2].scatter(month_diff, data[:, 2], c=data[:, 3], alpha=0.5)
    axs[2].set_xlabel("Days since last purchase")
    axs[2].set_ylabel("Average basket price")
    plt.show()


def bar_plot(data: np.ndarray):
    """Plots a bar plot to see the ammount of customer in each category"""

    labels = ["Silver", "Inactive", "New Customers", "Gold", "Bronze"]
    counts = []
    for i in range(0, len(labels)):
        counts.append(len(data[data[:, 3] == i]))

    fig, ax = plt.subplots()
    rects = ax.bar(labels, counts)
    ax.bar_label(rects, padding=3)
    ax.set_ylabel('Number of customers')
    plt.show()


if __name__ == "__main__":
    main()
