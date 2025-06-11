import pandas as pd
import matplotlib.pyplot as plt


TEST_FILE = "Test_knight.csv"
TRAIN_FILE = "Train_knight.csv"


def main():
    try:
        train_data = pd.read_csv(TRAIN_FILE)
        test_data = pd.read_csv(TEST_FILE)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        return 1

    scatter_plots(train_data, test_data)


def scatter_plots(train: pd.DataFrame, test: pd.DataFrame) -> None:
    """Creates the canvas and draws the 4 scatter plots"""

    fig, axs = plt.subplots(2, 2)

    plot_train_data(train, axs[0, 0], axs[0, 1])
    plot_test_data(test, axs[1, 0], axs[1, 1])

    plt.legend()
    plt.show()


def plot_train_data(data: pd.DataFrame, ax1: plt.Axes, ax2: plt.Axes) -> None:
    """Plots the scatter plots with distinction between jedi and Sith"""

    args = {"alpha": 0.5, "s": 30}
    jedi_args = {"c": "blue", "label": "jedi"}
    sith_args = {"c": "red", "label": "sith"}

    jedi = data[data["knight"] == "Jedi"]
    sith = data[data["knight"] == "Sith"]

    jedi.plot.scatter(x="Empowered", y="Stims", ax=ax1, **jedi_args, **args)
    sith.plot.scatter(x="Empowered", y="Stims", ax=ax1, **sith_args, **args)

    jedi.plot.scatter(x="Push", y="Deflection", ax=ax2, **jedi_args, **args)
    sith.plot.scatter(x="Push", y="Deflection", ax=ax2, **sith_args, **args)


def plot_test_data(data: pd.DataFrame, ax1: plt.Axes, ax2: plt.Axes) -> None:
    """Plots the scatter plots with no distinction between jedi and Sith"""

    args = {"alpha": 0.5, "s": 30, "c": "green", "label": "Knight"}

    data.plot.scatter(x="Empowered", y="Stims", ax=ax1, **args)
    data.plot.scatter(x="Push", y="Deflection", ax=ax2, **args)


if __name__ == "__main__":
    main()
