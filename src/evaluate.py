import pandas as pd
import tensorflow as tf
import pickle
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error
import argparse
import sys
import os
import warnings

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
warnings.filterwarnings("ignore")

cli_parser = argparse.ArgumentParser()
cli_parser.add_argument(
    "--datapath",
    nargs="?",
    default="data/preprocessed/test_data.csv"
)
cli_parser.add_argument( # optional argument  with default "None"
    "--aimodelpath", 
    # nargs="?",
    # default="learningBase/currentAiSolution.keras"
)
cli_parser.add_argument( # optional argument  with default "None"
    "--olsmodelpath",
    # nargs="?",
    # default="learningBase/currentOlsSolution.pkl"
)
cli_parser.add_argument( # optional argument  with default "None"
    "--printmse",
    default=False,
)
args = cli_parser.parse_args()#sys.argv)

df = pd.read_csv(args.datapath)
X = df.drop(columns=["target", "bundesland", "year"])
y = df["target"]


print(f"Groundtruth Target Value: {float(y.iat[0])}")

if args.aimodelpath is not None:
    nn = tf.keras.models.load_model(args.aimodelpath)
    nn_pred = nn.predict(X.values, verbose=0).flatten()
    if args.printmse:
        print("NN MSE :", mean_squared_error(y, nn_pred))
    print(f"ANN-Predicted Target Value: {nn_pred[0]}")

if args.olsmodelpath is not None:
    with open(args.olsmodelpath, "rb") as f:
        ols = pickle.load(f)
    X_ols = sm.add_constant(X, has_constant="add")
    ols_pred = ols.predict(X_ols)
    if args.printmse:
        print("OLS MSE:", mean_squared_error(y, ols_pred))
    print(f"OLS-Predicted Target Value: {ols_pred[0]}")


