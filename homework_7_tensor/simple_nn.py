import tensorflow as tf, numpy as np
tf.random.set_seed(42);  np.random.seed(42)


# super simple model that's deciding what pay per hour should I get
hours = np.array([[2], [5], [8]], dtype=np.float32)
pay   = np.array([[30], [75], [120]], dtype=np.float32)

lin_model = tf.keras.Sequential([
    tf.keras.layers.Dense(1, input_shape=(1,))
])
lin_model.compile(
    optimizer=tf.keras.optimizers.SGD(learning_rate=0.01), 
    loss="mse"
)
lin_model.fit(hours, pay, epochs=100, verbose=0)

w, b = lin_model.layers[0].get_weights()
print(f"\nLearned pay ≈ {w[0][0]:.2f} × hours + {b[0]:.2f}")


# trying out trained modeL:

while True:
    txt = input("\nEnter number of hours (blank to quit): ").strip()
    if txt == "":
        break
    try:
        h = float(txt)
    except ValueError:
        print("Please type a number like 3.5")
        continue
    pred_pay = lin_model.predict(np.array([[h]], dtype=np.float32), verbose=0)[0,0]
    print(f"Predicted pay: ${pred_pay:.2f}")
