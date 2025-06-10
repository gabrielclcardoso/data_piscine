import pandas as pd
import matplotlib.pyplot as plt

FILE = "Test_knight.csv"


def main():
    try:
        data = pd.read_csv(FILE)
        data.hist()
        plt.show()
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":
    main()
