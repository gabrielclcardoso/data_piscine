import sys

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer
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

    clf, accuracies = train_knn(features, targets)
    run_predictions(clf, test_data)

    get_f1_score(clf, features, targets)
    plot_accuracy(accuracies)


def standardize_data(train):
    """Standardizes the training data"""

    if train is not None:
        train_scaler = StandardScaler()
        numeric_cols = train.select_dtypes(include=np.number).columns
        train[numeric_cols] = train_scaler.fit_transform(train[numeric_cols])


def train_knn(features, targets):
    """Trains a decision tree based on the best parameters found with a
    GridSearchCV"""

    param_grid = {'n_neighbors': [i for i in range(1, 31)]}

    clf = KNeighborsClassifier()
    gs = GridSearchCV(estimator=clf, param_grid=param_grid, cv=6,
                      n_jobs=-1, verbose=1)
    gs.fit(features, targets)

    best_clf = gs.best_estimator_
    print(f"accuracy of the chosen number of neighbors: {gs.best_score_}")
    print(f"parameters chosen = {gs.best_params_}")

    results = pd.DataFrame(gs.cv_results_)
    gs.estimator

    return best_clf, results["mean_test_score"]


def run_predictions(clf, test_data):
    """Runs the decision tree on the testing data and writes the reults to a
    KNN.txt file"""

    predictions = clf.predict(test_data)
    content = '\n'.join(predictions)
    with open("KNN.txt", mode='w') as f:
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
