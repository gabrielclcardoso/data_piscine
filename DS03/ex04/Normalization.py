import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler


TEST_FILE = "Test_knight.csv"
TRAIN_FILE = "Train_knight.csv"


def main():
    try:
        test_data = pd.read_csv(TEST_FILE)
    except Exception:
        test_data = None

    try:
        train_data = pd.read_csv(TRAIN_FILE)
    except Exception:
        train_data = None

    try:
        assert train_data is not None or test_data is not None, \
            "No data received to plot"
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        return 1

    print_data(train_data, test_data)
    normalize_data(train_data, test_data)
    print_data(train_data, test_data)
    scatter_plot(train_data, test_data)


def print_data(train: pd.DataFrame, test: pd.DataFrame) -> None:
    """Prints the loaded dataframes"""

    if train is not None:
        print(train)
    if test is not None:
        print(test)


def normalize_data(train: pd.DataFrame, test: pd.DataFrame) -> None:
    """Standardizes the loaded dataframes"""

    if train is not None:
        train_scaler = MinMaxScaler()
        numeric_cols = train.select_dtypes(include=np.number).columns
        train[numeric_cols] = train_scaler.fit_transform(train[numeric_cols])

    if test is not None:
        test_scaler = MinMaxScaler()
        test[:] = test_scaler.fit_transform(test)


def scatter_plot(train: pd.DataFrame, test: pd.DataFrame) -> None:
    """Creates the canvas and draws the scatter plot for the loaded
    DataFrames"""

    if train is not None and test is not None:
        fig, axs = plt.subplots(1, 2)
        train_ax = axs[0]
        test_ax = axs[1]
    elif train is not None:
        fig, train_ax = plt.subplots()
    else:
        fig, test_ax = plt.subplots()

    if train is not None:
        plot_train_data(train, train_ax)
    if test is not None:
        plot_test_data(test, test_ax)

    plt.legend()
    plt.show()


def plot_train_data(data: pd.DataFrame, ax: plt.Axes) -> None:
    """Plots a scatter plot with different colors for jedi and Sith"""

    args = {"alpha": 0.5, "s": 50, "ax": ax}
    jedi_args = {"c": "blue", "label": "jedi"}
    sith_args = {"c": "red", "label": "sith"}

    jedi = data[data["knight"] == "Jedi"]
    sith = data[data["knight"] == "Sith"]

    jedi.plot.scatter(x="Push", y="Deflection", **jedi_args, **args)
    sith.plot.scatter(x="Push", y="Deflection", **sith_args, **args)


def plot_test_data(data: pd.DataFrame, ax: plt.Axes) -> None:
    """Plots the scatter plots with no distinction between jedi and Sith"""

    args = {"alpha": 0.5, "s": 50, "c": "green", "label": "Knight", "ax": ax}

    data.plot.scatter(x="Empowered", y="Stims", **args)


if __name__ == "__main__":
    main()
