import pandas as pd
import tensorflow as tf
import pickle
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error
import argparse
import sys
import os
import warnings
import matplotlib.pyplot as plt

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

train_dataset = pd.read_csv('data/preprocessed/training_data.csv')
df = pd.read_csv(args.datapath)
X = df.drop(columns=["target", "bundesland", "year"])
y = df["target"]

def plot_preds(predictions, model, X=X, y=y, df=train_dataset):
    X = X[['x_t-1']]
    fig = plt.figure()
    ax1 = fig.add_subplot()
    # plot predictions on test set
    
    #ax1.plot(X, predictions, color='red')
    ax1.scatter(X.values, y.values, color='blue', s=15)
    ax1.plot(X.values, predictions, color='red')
    ax1.scatter([df[['x_t-1']]],df[['target']], color='blue', s=15, label='Groundtruth')
    plt.xlabel("input")
    plt.ylabel("prediction")
    plt.title(f"Predictions on test set for model {model}")
    plt.savefig(f"data_visualization/output/predictions_{model}.png")
    return plt.show()

print(f"Groundtruth Target Value: {float(y.iat[0])}")

if args.aimodelpath is not None:
    nn = tf.keras.models.load_model(args.aimodelpath)
    nn_pred = nn.predict(X.values, verbose=0).flatten()
    if args.printmse:
        print("NN MSE :", mean_squared_error(y, nn_pred))
    print(f"ANN-Predicted Target Value: {nn_pred[0]}")
    plot_preds(nn_pred, model="ANN") 


if args.olsmodelpath is not None:
    with open(args.olsmodelpath, "rb") as f:
        ols = pickle.load(f)
    X_ols = sm.add_constant(X, has_constant="add")
    ols_pred = ols.predict(X_ols)
    if args.printmse:
        print("OLS MSE:", mean_squared_error(y, ols_pred))
    print(f"OLS-Predicted Target Value: {ols_pred[0]}")
    plot_preds(ols_pred, model="OLS") 



