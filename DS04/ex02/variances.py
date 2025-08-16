import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

TRAIN_FILE = "Train_knight.csv"


def main():
    try:
        train_data = pd.read_csv(TRAIN_FILE)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        return 1

    standardize_data(train_data)

    encoder = LabelEncoder()
    train_data["knight"] = encoder.fit_transform(train_data["knight"])

    pca = PCA()
    pca.fit(train_data)

    exp_var = pca.explained_variance_ratio_ * 100
    cum_var = np.cumsum(exp_var)

    print(f"Variances (Percentage):\n{exp_var}")
    print(f"Cumulative variances (Percentage)\n{cum_var}")

    plt.plot(cum_var)
    plt.ylabel("Explained Variance (%)")
    plt.xlabel("Number of components")
    plt.show()


def standardize_data(train: pd.DataFrame) -> None:
    """Standardizes the loaded dataframes"""

    train_scaler = StandardScaler()
    numeric_cols = train.select_dtypes(include=np.number).columns
    train[numeric_cols] = train_scaler.fit_transform(train[numeric_cols])


if __name__ == "__main__":
    main()
