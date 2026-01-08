import pandas as pd
import statsmodels.api as sm
import pickle
from pathlib import Path

DATA = "data/preprocessed/training_data.csv"
OUT = Path("learningBase/currentOlsSolution.pkl")
OUT.parent.mkdir(exist_ok=True)

df = pd.read_csv(DATA)
print(df.columns)
X = df.drop(columns=["target", "bundesland", "year"]) # year-unnormalized?
X = sm.add_constant(X)
y = df["target"]

model = sm.OLS(y, X).fit()


def _standardize_training_target(y_unstandardized):
    return (y_unstandardized - df["target"].mean()) / df["target"].std()

mse = pd.Series(
   (_standardize_training_target(model.predict()) - _standardize_training_target(y))**2
).mean()
print(f"MSE: {mse}\n\n")
print(model.summary())


with open(OUT, "wb") as f:
    pickle.dump(model, f)
