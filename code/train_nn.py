import pandas as pd
import tensorflow as tf
from pathlib import Path
import os
import warnings

# attempts to get rid of warnings:
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
warnings.filterwarnings("ignore")

DATA = "data/preprocessed/training_data.csv"
MODEL_OUT = Path("learningBase/currentAiSolution.keras")
MODEL_OUT.parent.mkdir(exist_ok=True)

df = pd.read_csv(DATA)

X = df.drop(columns=["target", "bundesland", "year"]).values

y_mean = df["target"].mean()
y_std = df["target"].std()
y = (df["target"] - y_mean) / y_std


model = tf.keras.Sequential([
    tf.keras.Input(shape=(X.shape[1],)),
    tf.keras.layers.Dense(16, activation="relu"),
    tf.keras.layers.Dense(8, activation="relu"),
    tf.keras.layers.Dense(1)
])

model.compile(
    optimizer="adam",
    loss="mse",
    metrics=["mae"]
)

history = model.fit(X, y, epochs=120, batch_size=8, verbose=0)

print(history.history["loss"])#,history.history["metrics"])

model.save(MODEL_OUT)

print(f"\n\nSUCCESFULLY SAVED TRAINED MODEL TO {MODEL_OUT}\n\n")