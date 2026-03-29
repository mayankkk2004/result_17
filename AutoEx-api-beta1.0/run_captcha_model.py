from tensorflow.keras.models import load_model

model = load_model("captcha_model.hdf5")
print("✅ captcha_model.hdf5 successfully load ho gaya")
model.summary()
