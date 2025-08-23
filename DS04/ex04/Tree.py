import sys

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn.metrics import f1_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer


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

    clf = train_decision_tree(features, targets)
    run_predictions(clf, test_data)

    plot_tree(clf, features)


def train_decision_tree(features, targets):
    """Trains a decision tree based on the best parameters found with a
    GridSearchCV"""

    param_grid = {
        'max_depth': [3, 4, 5, 6, 7, 8],
        'min_samples_leaf': [5, 10, 15, 20],
        'min_samples_split': [10, 20, 30, 40],
        'criterion': ['gini', 'entropy']
    }
    scorer = make_scorer(f1_score, pos_label='Jedi')

    dt = DecisionTreeClassifier(random_state=0)
    gs = GridSearchCV(estimator=dt, param_grid=param_grid, cv=5,
                      n_jobs=-1, verbose=1, scoring=scorer)
    gs.fit(features, targets)

    best_tree = gs.best_estimator_
    print(
        f"Mean cross validated f1-score of the chosen tree: {gs.best_score_}")
    print(f"parameters chosen = {gs.best_params_}")

    return best_tree


def run_predictions(clf, test_data):
    """Runs the decision tree on the testing data and writes the reults to a
    Tree.txt file"""

    predictions = clf.predict(test_data)
    content = '\n'.join(predictions)
    with open("Tree.txt", mode='w') as f:
        f.write(content)


def plot_tree(clsifier, features):
    """Plots the decision tree and creates an svg file of the plot"""

    tree.plot_tree(clsifier, filled=True, feature_names=features.columns,
                   class_names=["Jedi", "Sith"])
    plt.savefig('decision_tree.svg', format='svg', bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    main()
