import pandas as pd
import tensorflow as tf
from pathlib import Path
import os
import warnings
import keras
from keras.layers import Dropout
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

# attempts to get rid of harmless warnings from tensorflow:
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
warnings.filterwarnings("ignore")

DATA = "data/preprocessed/training_data.csv"
MODEL_OUT = Path("learningBase/currentAiSolution.keras")

@keras.saving.register_keras_serializable("train_nn") # required for serialization of NN
class RescaleLayer(tf.keras.layers.Layer):
    def __init__(self, mean, std, **kwargs):
        super().__init__(**kwargs)
        self.mean = mean
        self.std = std
    def call(self, inputs, training=False, validation=False):
        if validation:
            return inputs
        if training:
            return inputs  # pass through during training
        else:
            return inputs * self.std + self.mean
    def get_config(self): # required for register_keras_serializable()
        config = super().get_config()
        config.update({"mean": self.mean, "std": self.std, })
        return config
    
if __name__ == "__main__":
    MODEL_OUT.parent.mkdir(exist_ok=True)

    # load data
    df = pd.read_csv(DATA)

    df_y = df.target
    df_X = df.drop(columns=["target", "bundesland", "year"])
    df_X= df_X.values

    # Split X and Y values into training and validation
    X_train, X_val = train_test_split(df_X, test_size=0.2, shuffle=False)
    Y_train, Y_val = train_test_split(df_y, test_size=0.2, shuffle=False)

    # rescale targets for efficient training, add rescaling layer only applying at application time
    Y_train = (Y_train - Y_train.mean()) / Y_train.std()
    Y_val = (Y_val - Y_val.mean()) / Y_val.std()

    model = tf.keras.Sequential([
        tf.keras.Input(shape=(X_train.shape[1],)),
        tf.keras.layers.Dense(8, activation="relu"),
        Dropout(0.3),
        tf.keras.layers.Dense(8, activation="relu"),
        tf.keras.layers.Dense(1),
        RescaleLayer(Y_train.mean(), Y_train.std()),
    ])
    model.compile(
        optimizer="adam",
        loss="mse",
    )

    model.summary()
    history = model.fit(X_train, Y_train, epochs=100, batch_size=8, verbose=1, validation_data=(X_val, Y_val))

    loss = history.history["loss"]
    val_loss = history.history["val_loss"]

    ax, fig = plt.subplots()
    plt.plot(loss, label="Training Loss")
    plt.plot(val_loss, label="Validation Loss")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()
    plt.savefig("train_val_loss.png")

    model.save(MODEL_OUT)

    print(f"\n\nSUCCESSFULLY SAVED TRAINED MODEL TO {MODEL_OUT}\n\n")