import pandas as pd
import matplotlib.pyplot as plt

TEST_FILE = "Test_knight.csv"
TRAIN_FILE = "Train_knight.csv"


def main():
    try:
        test_data = pd.read_csv(TEST_FILE)
        train_data = pd.read_csv(TRAIN_FILE)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        return 1

    plot_general_histograms(test_data)
    plot_comparative_histograms(train_data)

    plt.subplots_adjust(hspace=0.55, top=0.95,
                        bottom=0.05, left=0.02, right=0.98)
    plt.show()


def plot_general_histograms(data: pd.DataFrame) -> None:
    """Plots exploratory histograms for the testing data"""

    data.hist(color="lightgreen", label="Knight", bins=20)
    plt.subplots_adjust(hspace=0.55, top=0.95,
                        bottom=0.05, left=0.02, right=0.98)
    plt.legend()


def plot_comparative_histograms(data: pd.DataFrame) -> None:
    """Plots exploratory histograms for the training data"""

    sith = data[data["knight"] == "Sith"]
    jedi = data[data["knight"] == "Jedi"]

    fig, axes = plt.subplots(6, 5)
    jedi.hist(ax=axes, color="blue", label="Jedi", alpha=0.5, bins=20)
    sith.hist(ax=axes, color="red", label="Sith", alpha=0.5, bins=20)
    plt.legend()


if __name__ == "__main__":
    main()
