import sys

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn import tree
from sklearn.metrics import f1_score


def main():
    try:
        assert len(sys.argv) == 3, "Missing file paths in the cmd"
        train_data = pd.read_csv(sys.argv[1])
        test_data = pd.read_csv(sys.argv[2])
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        return 1

    features = train_data.drop(columns="knight")
    targets = train_data["knight"]

    decision_tree = train_decision_tree(features, targets)
    predictions = run_predictions(decision_tree, test_data)

    try:
        print_f1_score(predictions)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        return 1

    # plot_tree(decision_tree, features)


def train_decision_tree(features, targets):
    """Trains a decision tree based on the features and targets provided
    and prints it's cross validation score2"""

    decision_tree = DecisionTreeClassifier(random_state=0)
    decision_tree.fit(features, targets)

    score = cross_val_score(decision_tree, features, targets, cv=10)
    print(f"Cross Validation scores for decision tree:\n{score}")

    return decision_tree


def run_predictions(decision_tree, test_data):
    """Runs the decision tree on the testing data and writes the reults to a
    prediction.txt file"""

    predictions = decision_tree.predict(test_data)
    content = '\n'.join(predictions)
    with open("prediction.txt", mode='w') as f:
        f.write(content)

    return predictions


def print_f1_score(predictions):
    """Gets the correct predictions from a truth.txt file and prints the
    f1 score of the given predictions"""

    with open("truth.txt") as f:
        truth = [line.strip() for line in f]

    print(f"{len(truth)} vs {len(predictions[:len(truth)])}")
    score = f1_score(truth, predictions[:len(truth)], pos_label="Sith")
    print(f"f1 score = {score:.2f}")


def plot_tree(clsifier, features):
    """Plots the decision tree and creates an svg file of the plot"""

    tree.plot_tree(clsifier, filled=True, feature_names=features.columns,
                   class_names=["Jedi", "Sith"])
    plt.savefig('decision_tree.svg', format='svg', bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    main()
