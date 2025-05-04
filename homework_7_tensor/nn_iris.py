#!/usr/bin/env python3
"""
deap_iris.py

Tiny supervised‑learning demo that uses **DEAP** to evolve a mini‑MLP for the classic
Iris flower‑classification dataset (downloaded from *TensorFlow Datasets*).

With only 150 samples and 4 numeric features, this is about the simplest
non‑vision benchmark you can get.  After a quick 4‑generation hyper‑parameter
search the best model is retrained and reaches > 95 % accuracy on the held‑out
test split.
"""

import random
import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
from deap import base, creator, tools, algorithms

# Loads Iris dataset and prepare train / validation / test
# --------------------------------------------------------------------------------------

ds_all = tfds.load("iris", split="train", as_supervised=True, shuffle_files=True)

data = list(tfds.as_numpy(ds_all))
random.shuffle(data)

X, y = zip(*data)
X = np.stack(X).astype("float32")
y = np.array(y, dtype="int32")

y_onehot = tf.keras.utils.to_categorical(y, num_classes=3)

# 60‑20‑20 split  (90 train, 30 val, 30 test)
train_idx = int(0.6 * len(X))
val_idx = int(0.8 * len(X))

X_train, y_train = X[:train_idx], y_onehot[:train_idx]
X_val, y_val     = X[train_idx:val_idx], y_onehot[train_idx:val_idx]
X_test, y_test   = X[val_idx:], y_onehot[val_idx:]

BATCH = 16
train_ds = tf.data.Dataset.from_tensor_slices((X_train, y_train)).batch(BATCH)
val_ds   = tf.data.Dataset.from_tensor_slices((X_val,   y_val  )).batch(BATCH)

test_ds  = tf.data.Dataset.from_tensor_slices((X_test,  y_test )).batch(BATCH)

# --------------------------------------------------------------------------------------
# 2  Build‑model helper
# --------------------------------------------------------------------------------------

HIDDEN_SIZES   = [4, 8, 16, 32]
LEARNING_RATES = [1e-2, 5e-3, 1e-3]
SEARCH_EPOCHS  = 20  # iris trains almost instantly


def build_model(units: int, lr: float) -> tf.keras.Model:
    model = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=(4,)),
            tf.keras.layers.Dense(units, activation="relu"),
            tf.keras.layers.Dense(3, activation="softmax"),
        ]
    )
    model.compile(
        optimizer=tf.keras.optimizers.Adam(lr),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model

# --------------------------------------------------------------------------------------
# 3  Set up DEAP GA
# --------------------------------------------------------------------------------------

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("attr_units", random.randrange, len(HIDDEN_SIZES))
toolbox.register("attr_lr",    random.randrange, len(LEARNING_RATES))

toolbox.register("individual", tools.initCycle, creator.Individual,
                 (toolbox.attr_units, toolbox.attr_lr), n=1)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def evaluate(ind):
    units = HIDDEN_SIZES[ind[0]]
    lr    = LEARNING_RATES[ind[1]]
    model = build_model(units, lr)
    model.fit(train_ds, epochs=SEARCH_EPOCHS, verbose=0)
    loss, acc = model.evaluate(val_ds, verbose=0)
    return (acc,)


toolbox.register("evaluate", evaluate)

toolbox.register("mate", tools.cxOnePoint)

toolbox.register(
    "mutate",
    tools.mutUniformInt,
    low=[0, 0],
    up=[len(HIDDEN_SIZES) - 1, len(LEARNING_RATES) - 1],
    indpb=0.3,
)

toolbox.register("select", tools.selTournament, tournsize=3)

# --------------------------------------------------------------------------------------
# 4  Run GA and final training
# --------------------------------------------------------------------------------------

def main():
    pop = toolbox.population(n=12)
    hof = tools.HallOfFame(1)

    stats = tools.Statistics(lambda ind: ind.fitness.values[0])
    stats.register("avg", np.mean)
    stats.register("max", np.max)

    algorithms.eaSimple(pop, toolbox, cxpb=0.6, mutpb=0.3, ngen=4, stats=stats,
                        halloffame=hof, verbose=True)

    best = hof[0]
    cfg = dict(units=HIDDEN_SIZES[best[0]], lr=LEARNING_RATES[best[1]])
    print("\nBest hyper‑parameters:", cfg)
    
    full_ds = train_ds.concatenate(val_ds)

    final_model = build_model(**cfg)
    final_model.fit(
                full_ds,
                epochs=100,
                verbose=0,
                callbacks=[
                    tf.keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True)
                ],
            )

    loss, acc = final_model.evaluate(test_ds, verbose=0)
    print(f"\nTest accuracy: {acc:.2%}")

if __name__ == "__main__":
    main()
