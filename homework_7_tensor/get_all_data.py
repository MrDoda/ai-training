# 1) TensorFlow Datasets  – one-liner
import tensorflow_datasets as tfds
ds_train = tfds.load("iris", split="train")      # gives 150 examples

# 2) Direct CSV  – pandas + NumPy
import pandas as pd
url = "https://storage.googleapis.com/download.tensorflow.org/data/iris_training.csv"
cols = ["sepal_length", "sepal_width", "petal_length", "petal_width", "species"]
df = pd.read_csv(url, names=cols, header=0)

# 3) UCI raw file  – plain text
import pandas as pd
raw_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
df = pd.read_csv(raw_url, names=cols)
