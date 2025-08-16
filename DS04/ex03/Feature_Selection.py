import pandas as pd
import numpy as np

from statsmodels.stats.outliers_influence import variance_inflation_factor

TRAIN_FILE = "Train_knight.csv"


def main():
    try:
        train_data = pd.read_csv(TRAIN_FILE)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        return 1

    numeric_cols = train_data.select_dtypes(include=np.number).columns
    features = train_data[numeric_cols]

    features = reduce_features(features, 5)
    print(f"\nFinal Features:\n{features.columns}")


def calculate_vif(features: pd.DataFrame) -> pd.DataFrame:
    """Calculates the VIF and Tolerance of each feature"""

    vif = pd.DataFrame(index=features.columns)
    vif["VIF"] = [variance_inflation_factor(features.values, i)
                  for i in range(len(features.columns))]
    vif["Tolerance"] = 1 / vif["VIF"]

    return vif


def reduce_features(features: pd.DataFrame, threshhold: int) -> pd.DataFrame:
    """Reduces the number of features until the VIF goes below threshhold"""

    vif = calculate_vif(features)
    print(f"Iinitial Values:\n{vif}\n")

    while (max(vif["VIF"]) >= threshhold):
        f = vif["VIF"].idxmax()
        print(f"Removing feature {f} with VIF = {vif["VIF"][f]:.2f}")
        features = features.drop(vif["VIF"].idxmax(), axis=1)
        vif = calculate_vif(features)

    return features


if __name__ == "__main__":
    main()
