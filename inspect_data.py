import pandas as pd
import pickle

# Load the data
df = pd.read_csv('Training.csv')
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# Check the prognosis data
print("Prognosis column data type:", df['prognosis'].dtype)
print("First 10 prognosis values:", df['prognosis'].head(10).tolist())
print("Unique prognosis values:", df['prognosis'].unique().tolist())

# Load the model and check predictions 
with open('new_disease_prediction_system.pkl', 'rb') as f:
    data = pickle.load(f)

# Create a sample input with no symptoms
sample_input = pd.DataFrame(0, index=[0], columns=df.columns.drop('prognosis'))

# Test prediction with the random forest model
rf_model = data["final_rf_model"]
prediction = rf_model.predict(sample_input)[0]
print("\nRandom Forest prediction type:", type(prediction))
print("Random Forest prediction value:", prediction)

# Print the classes the model knows about
if hasattr(rf_model, 'classes_'):
    print("\nClasses in the RF model:")
    print("Type:", type(rf_model.classes_))
    print("Values:", rf_model.classes_) 