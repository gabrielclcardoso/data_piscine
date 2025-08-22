import sys

import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score


REDUCED_FEATURES = ["Push", "Lightsaber", "Friendship", "Attunement"]


def main():
    try:
        assert len(sys.argv) == 3, "Missing file paths in the cmd"
        train_data = pd.read_csv(sys.argv[1])
        test_data = pd.read_csv(sys.argv[2])
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        return 1

    features = train_data[REDUCED_FEATURES]
    targets = train_data["knight"]

    decision_tree = train_decision_tree(features, targets)


def train_decision_tree(features, targets):
    """Trains a decision tree based on the features and targets provided
    and prints it's cross validation score2"""

    tree = DecisionTreeClassifier(random_state=0)
    tree.fit(features, targets)

    score = cross_val_score(tree, features, targets, cv=10)
    print(f"Cross Validation scores for decision tree:\n{score}")

    return tree


if __name__ == "__main__":
    main()
