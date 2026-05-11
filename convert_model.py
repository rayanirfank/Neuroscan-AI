from tensorflow.keras.models import load_model

model = load_model("brain_tumor_model.h5")

model.save("brain_tumor_model.keras")

print("Model converted successfully")