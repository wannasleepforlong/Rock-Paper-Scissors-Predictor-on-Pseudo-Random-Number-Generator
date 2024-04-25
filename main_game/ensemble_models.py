import numpy as np
import matplotlib.pyplot as plt
import sklearn

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
import numpy as np

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

reg1 = DecisionTreeRegressor()
reg2 = RandomForestRegressor()
reg3 = GradientBoostingRegressor()
reg4 = MLPRegressor()

reg1.fit(X_train, y_train)
reg2.fit(X_train, y_train)
reg3.fit(X_train, y_train)
reg4.fit(X_train, y_train)

predictions = []
models = [reg1, reg2, reg3, reg4]  

for model in models:
    predictions.append(model.predict_proba(X_test))

predictions = np.array(predictions)

best_model_indices = np.argmax(predictions, axis=0)

ensemble_predictions = [model_index[input_index] for input_index, model_index in enumerate(best_model_indices)]

accuracy = accuracy_score(y_test, ensemble_predictions)
print("Ensemble Accuracy:", accuracy)
