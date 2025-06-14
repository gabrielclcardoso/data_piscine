import pandas as pd
from sklearn.model_selection import train_test_split


TRAIN_FILE = "Train_knight.csv"


def main():
    try:
        data = pd.read_csv(TRAIN_FILE)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        return 1

    train, validation = train_test_split(
        data, test_size=0.2, stratify=data['knight'])

    try:
        train.to_csv("Training_knight.csv")
        validation.to_csv("Validation_knight.csv")
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":
    main()
