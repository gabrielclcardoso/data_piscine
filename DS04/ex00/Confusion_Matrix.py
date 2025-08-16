import sys

import numpy as np
import matplotlib.pyplot as plt


def main():
    assert len(sys.argv) == 3, "File path missing"

    with open(sys.argv[1], 'r') as p, open(sys.argv[2], 'r') as t:
        predictions = [line.strip() for line in p]
        truths = [line.strip() for line in t]

        predictions = [label_to_number(i) for i in predictions]
        truths = [label_to_number(i) for i in truths]

        confusion_matrix = cf_matrix(predictions, truths)
        print_data(predictions, truths, confusion_matrix)
        plot_data(confusion_matrix)


def label_to_number(s: str):
    """Converts the variable Knight to a binary"""

    if s == "Sith":
        return 0
    elif s == "Jedi":
        return 1

    raise Exception("Invalid data received")


def cf_matrix(predictions: list, truths: list):
    """Creates a confusion matrix based on the predictions and truths"""

    cf_matrix = [[0, 0], [0, 0]]

    for p, t in zip(predictions, truths):
        if t == 1:
            if p == 1:
                cf_matrix[0][0] += 1
            elif p == 0:
                cf_matrix[0][1] += 1
        elif t == 0:
            if p == 1:
                cf_matrix[1][0] += 1
            elif p == 0:
                cf_matrix[1][1] += 1

    return cf_matrix


def print_data(predictions: list, truths: list, cm: list):
    jp = cm[0][0] / (cm[0][0] + cm[1][0])
    jr = cm[0][0] / truths.count(1)
    jf1 = 2*cm[0][0] / (2*cm[0][0] + cm[1][0] + cm[0][1])

    sp = cm[1][1] / (cm[1][1] + cm[0][1])
    sr = cm[1][1] / truths.count(0)
    sf1 = 2*cm[1][1] / (2*cm[1][1] + cm[0][1] + cm[1][0])

    acc = (cm[0][0] + cm[1][1]) / len(truths)

    print("\tprecision\trecall\tf1-score\ttotal")
    print(f"Jedi\t{jp:.2}\t\t{jr:.2}\t{jf1:.2}\t\t{truths.count(1)}")
    print(f"Sith\t{sp:.2}\t\t{sr:.2}\t{sf1:.2}\t\t{truths.count(0)}")
    print(f"accuracy\t\t\t{acc:.2}\t\t{len(truths)}")


def plot_data(cm: list):
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion Matrix')
    plt.colorbar()
    tick_marks = np.arange(2)

    plt.xticks(tick_marks, ['0', '1'])
    plt.yticks(tick_marks, ['0', '1'], rotation=90)

    plt.text(0, 0, format(cm[0][0], 'd'), horizontalalignment="center",
             color="black")
    plt.text(0, 1, format(cm[0][1], 'd'), horizontalalignment="center",
             color="black")
    plt.text(1, 0, format(cm[1][0], 'd'), horizontalalignment="center",
             color="black")
    plt.text(1, 1, format(cm[1][1], 'd'), horizontalalignment="center",
             color="black")

    plt.show()


if __name__ == "__main__":
    main()
