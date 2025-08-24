import sys

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import make_scorer, f1_score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score


def main():
    try:
        assert len(sys.argv) == 3, "Missing file paths in the cmd"
        train_data = pd.read_csv(sys.argv[1])
        test_data = pd.read_csv(sys.argv[2])
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        return 1

    standardize_data(train_data)

    features = train_data.drop(columns="knight")
    targets = train_data["knight"]

    classifiers = []

    classifiers.append(("dt", get_decision_tree()))
    classifiers.append(("KNN", KNeighborsClassifier(n_neighbors=7)))
    classifiers.append(("lr", LogisticRegression(random_state=0)))

    voting_clf = VotingClassifier(estimators=classifiers)
    voting_clf.fit(features, targets)

    run_predictions(voting_clf, test_data)

    get_f1_score(voting_clf, features, targets)


def standardize_data(train):
    """Standardizes the training data"""

    if train is not None:
        train_scaler = StandardScaler()
        numeric_cols = train.select_dtypes(include=np.number).columns
        train[numeric_cols] = train_scaler.fit_transform(train[numeric_cols])


def get_decision_tree():
    """Creates a decision tree with the following parameters:
    ['criterion': 'entropy', 'max_depth': 3, 'min_samples_leaf': 15,
    'min_samples_split': 10]"""

    parameters = {
        "criterion": "entropy", "max_depth": 3, "random_state": 0,
        "min_samples_leaf": 15, "min_samples_split": 10
    }

    clf = DecisionTreeClassifier(**parameters)

    return clf


def run_predictions(clf, test_data):
    """Runs the decision tree on the testing data and writes the reults to a
    Voting.txt file"""

    predictions = clf.predict(test_data)
    content = '\n'.join(predictions)
    with open("Voting.txt", mode='w') as f:
        f.write(content)


def get_f1_score(clf, features, targets):
    """Performs cross validation with f1-score as a measurer"""

    scorer = make_scorer(f1_score, pos_label='Jedi')
    scores = cross_val_score(clf, features, targets, cv=10, scoring=scorer)
    print(f"Mean f1-score = {sum(scores) / len(scores)}")


def plot_accuracy(accuracies):
    """Plots the mean accuracy for each chosen K"""

    plt.plot(range(1, len(accuracies)+1), accuracies)
    plt.xlabel("k values")
    plt.ylabel("mean accuracy")
    plt.show()


if __name__ == "__main__":
    main()
