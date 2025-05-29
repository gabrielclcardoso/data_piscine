import psycopg
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

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

    wcss = elbow_method(data)
    plot_elbow(wcss)


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


def elbow_method(data: list[psycopg.rows.Row]) -> list[float]:
    """Performs kemans clustering for number of clusters 1 through 10"""

    scaled_data = StandardScaler().fit_transform(np.array(data))
    wcss = []
    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i).fit(np.array(scaled_data))
        wcss.append(kmeans.inertia_)
    return wcss


# Number of clusters chosen was 4
def plot_elbow(wcss: list[float]) -> None:
    """Plots the elbow with the values of wcss"""

    fig, ax = plt.subplots()
    n_clusters = list(range(1, len(wcss)+1))

    ax.grid(True)
    ax.set_xlabel("Number of clusters")
    ax.set_ylabel("within-cluster sum-of-squares")
    ax.set_title("The Elbow Method")

    ax.plot(n_clusters, wcss, zorder=2)

    plt.show()


if __name__ == "__main__":
    main()
