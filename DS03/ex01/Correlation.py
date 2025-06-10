import pandas as pd
from sklearn.preprocessing import LabelEncoder

TEST_FILE = "Test_knight.csv"
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
    print(corr["knight"].sort_values(ascending=False))


if __name__ == "__main__":
    main()
