import pandas as pd
import tensorflow as tf
from pathlib import Path
import os
import warnings
import keras
# attempts to get rid of harmless warnings from tensorflow:
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
warnings.filterwarnings("ignore")

DATA = "data/preprocessed/training_data.csv"
MODEL_OUT = Path("learningBase/currentAiSolution.keras")
MODEL_OUT.parent.mkdir(exist_ok=True)


df = pd.read_csv(DATA)

df_x = df.drop(columns=["target", "bundesland", "year"]) # NOTE: drop "year-normalized"? cf. preprocess: if dropped here, do not normalize "year" in preprocess.py at all
X = df_x.values


# rescale targets for efficient training, add rescaling layer only applying at application time
y_mean = df["target"].mean()
y_std = df["target"].std()
y = (df["target"] - y_mean) / y_std

@keras.saving.register_keras_serializable("train_nn") # required for serialization of NN
class RescaleLayer(tf.keras.layers.Layer):
    def __init__(self, mean, std, **kwargs):
        super().__init__(**kwargs)
        self.mean = mean
        self.std = std
    def call(self, inputs, training=False):
        if training:
            return inputs  # pass through during training
        else:
            return inputs * self.std + self.mean
    def get_config(self): # required for register_keras_serializable()
        config = super().get_config()
        config.update({"mean": self.mean, "std": self.std, })
        return config

model = tf.keras.Sequential([
    tf.keras.Input(shape=(X.shape[1],)),
    tf.keras.layers.Dense(16, activation="relu"),
    tf.keras.layers.Dense(8, activation="relu"),
    tf.keras.layers.Dense(1),
    RescaleLayer(y_mean, y_std),
])

model.compile(
    optimizer="adam",
    loss="mse",
    metrics=["mae"]
)

history = model.fit(X, y, epochs=100, batch_size=8, verbose=0)

print(history.history["loss"])#,history.history["metrics"])

model.save(MODEL_OUT)

print(f"\n\nSUCCESFULLY SAVED TRAINED MODEL TO {MODEL_OUT}\n\n")