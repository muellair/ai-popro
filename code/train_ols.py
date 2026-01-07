import pandas as pd
import statsmodels.api as sm
import pickle
from pathlib import Path

DATA = "data/preprocessed/training_data.csv"
OUT = Path("learningBase/currentOlsSolution.xml")
OUT.parent.mkdir(exist_ok=True)

df = pd.read_csv(DATA)

X = df.drop(columns=["target", "state"])
X = sm.add_constant(X)
y = df["target"]

model = sm.OLS(y, X).fit()

with open(OUT, "wb") as f:
    pickle.dump(model, f)
