import numpy as np
import pandas as pd
import cell
import grid
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import RidgeClassifier
from sklearn.metrics import accuracy_score, classification_report

url = "https://archive.ics.uci.edu/ml/machine-learning-databases/mushroom/agaricus-lepiota.data"
column_names = [
    'class', 'cap-shape', 'cap-surface', 'cap-color', 'bruises', 'odor',
    'gill-attachment', 'gill-spacing', 'gill-size', 'gill-color',
    'stalk-shape', 'stalk-root', 'stalk-surface-above-ring',
    'stalk-surface-below-ring', 'stalk-color-above-ring',
    'stalk-color-below-ring', 'veil-type', 'veil-color', 'ring-number',
    'ring-type', 'spore-print-color', 'population', 'habitat'
]

mushroom_data = pd.read_csv(url, header=None, names=column_names)

X = mushroom_data.drop('class', axis=1)
y = mushroom_data['class']

# Encode labels
encoder = LabelEncoder()
for column in X.columns:
    X[column] = encoder.fit_transform(X[column])
y = encoder.fit_transform(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert to binary format
X_train_binary = np.unpackbits(X_train.values.astype(np.uint8), axis=1)[:, :35]
X_test_binary = np.unpackbits(X_test.values.astype(np.uint8), axis=1)[:, :35]

# Create 35x35 grid and randomize
plate = grid.Grid(35)
plate.randomize_plate(percent_nor_fill=0.4, percent_wire_fill=0.5)

# Pass train and test data through
train_outputs = []
test_outputs = []
for x_i in X_train_binary:
    plate.inputs = x_i
    plate.update_plate()
    tmp_outputs = plate.set_outputs()
    train_outputs.append(tmp_outputs)

for x_i in X_test_binary:
    plate.inputs = x_i
    plate.update_plate()
    tmp_outputs = plate.set_outputs()
    test_outputs.append(tmp_outputs)

# Run ridge regression to test learning
ridge_classifier = RidgeClassifier(alpha=1.0, random_state=42)
ridge_classifier.fit(train_outputs, y_train)
y_pred = ridge_classifier.predict(test_outputs)

# Evaluate
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")

# Print detailed classification report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# If you want to see the coefficients of the model
print("\nModel Coefficients:")
for i, coef in enumerate(ridge_classifier.coef_[0]):
    print(f"Feature {i+1}: {coef:.4f}")


