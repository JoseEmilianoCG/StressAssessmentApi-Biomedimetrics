import os
import joblib

# Importación de modelo ML
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, 'stressmodelv2.pkl')
model = joblib.load(model_path)

print(model_path)

def predict(data):
    prediction = model.predict(data)
    return prediction
