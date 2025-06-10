import pandas as pd
import matplotlib.pyplot as plt

FILE = "Test_knight.csv"


def main():
    try:
        data = pd.read_csv(FILE)
        data.hist()
        plt.subplots_adjust(hspace=0.55, top=0.95,
                            bottom=0.05, left=0.02, right=0.98)
        plt.show()
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":
    main()
