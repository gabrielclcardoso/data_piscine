import pandas as pd
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

TRAIN_FILE = "Train_knight.csv"


def main():
    try:
        train_data = pd.read_csv(TRAIN_FILE)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        return 1

    encoder = LabelEncoder()
    train_data["knight"] = encoder.fit_transform(train_data["knight"])

    corr = train_data.corr()

    sns.heatmap(data=corr)
    plt.show()


if __name__ == "__main__":
    main()
