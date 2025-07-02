import csv               # For reading CSV files
import sys               # For handling command-line arguments

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4         # Fraction of data to use for testing (40%)


def main():
    # Ensure exactly one command-line argument is provided
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load evidence and labels from the CSV file
    evidence, labels = load_data(sys.argv[1])
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train the classifier and make predictions on test set
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)

    # Evaluate the predictions
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print out results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    # Initialize containers
    evidence = []
    labels = []

    # Map month abbreviations and full names to numerical indices
    month_map = {
        "Jan": 0, "January": 0,
        "Feb": 1, "February": 1,
        "Mar": 2, "March": 2,
        "Apr": 3, "April": 3,
        "May": 4,
        "Jun": 5, "June": 5,
        "Jul": 6, "July": 6,
        "Aug": 7, "August": 7,
        "Sep": 8, "September": 8,
        "Oct": 9, "October": 9,
        "Nov": 10, "November": 10,
        "Dec": 11, "December": 11
    }

    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert each field to the proper type and append to evidence
            evidence.append([
                int(row["Administrative"]),                            # 0
                float(row["Administrative_Duration"]),                 # 1
                int(row["Informational"]),                             # 2
                float(row["Informational_Duration"]),                  # 3
                int(row["ProductRelated"]),                            # 4
                float(row["ProductRelated_Duration"]),                 # 5
                float(row["BounceRates"]),                             # 6
                float(row["ExitRates"]),                               # 7
                float(row["PageValues"]),                              # 8
                float(row["SpecialDay"]),                              # 9
                month_map[row["Month"]],                               # 10
                int(row["OperatingSystems"]),                          # 11
                int(row["Browser"]),                                   # 12
                int(row["Region"]),                                    # 13
                int(row["TrafficType"]),                               # 14
                1 if row["VisitorType"] == "Returning_Visitor" else 0, # 15
                1 if row["Weekend"] == "TRUE" else 0                   # 16
            ])
            # Label: 1 if Revenue is TRUE, else 0
            labels.append(1 if row["Revenue"] == "TRUE" else 0)

    return evidence, labels


def train_model(evidence, labels):
    # Initialize KNN classifier with k = 1 (closest neighbor)
    model = KNeighborsClassifier(n_neighbors=1)
    # Train model on provided data
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    # Count true positives, true negatives, false positives, false negatives
    tp = tn = fp = fn = 0
    for actual, pred in zip(labels, predictions):
        if actual == 1 and pred == 1:
            tp += 1
        elif actual == 0 and pred == 0:
            tn += 1
        elif actual == 0 and pred == 1:
            fp += 1
        elif actual == 1 and pred == 0:
            fn += 1

    # Calculate sensitivity (TPR) and specificity (TNR)
    sensitivity = tp / (tp + fn)
    specificity = tn / (tn + fp)
    return sensitivity, specificity


if __name__ == "__main__":
    main()
