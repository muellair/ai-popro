import pandas as pd
import tensorflow as tf
import pickle
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error
from train_nn import RescaleLayer # necessary for deserialization of NN model

TEST = "data/preprocessed/test_data.csv"

df = pd.read_csv(TEST)
X = df.drop(columns=["target", "bundesland", "year"])
y = df["target"]

# NN
nn = tf.keras.models.load_model("learningBase/currentAiSolution.keras")
nn_pred = nn.predict(X.values, verbose=0).flatten()

# OLS
with open("learningBase/currentOlsSolution.pkl", "rb") as f:
    ols = pickle.load(f)

X_ols = sm.add_constant(X)
ols_pred = ols.predict(X_ols)

print("NN MSE :", mean_squared_error(y, nn_pred))
print("OLS MSE:", mean_squared_error(y, ols_pred))
