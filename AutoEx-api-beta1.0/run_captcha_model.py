from tensorflow.keras.models import load_model

try:
    model = load_model("captcha_model.hdf5")
    print("✅ captcha_model.hdf5 successfully loaded")
    model.summary()
except Exception as e:
    print(f"❌ Could not load model: {e}")
    print("Note: Re-upload captcha_model.hdf5 as a proper binary file (see .gitattributes).")
