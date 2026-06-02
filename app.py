from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
import pandas as pd
from sklearn.svm import SVC
from collections import Counter

app = Flask(__name__)

# Load the newly trained model
with open('new_disease_prediction_system.pkl', 'rb') as model_file:
    data_dict = pickle.load(model_file)

# Load symptoms from Training.csv
df = pd.read_csv('Training.csv')
# Remove any unnamed columns
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
symptoms = list(df.columns)
symptoms.remove('prognosis')  # Remove the target variable

# Train SVM model
if 'final_svm_model' not in data_dict:
    X = df.drop('prognosis', axis=1)
    y = df['prognosis']
    svm_model = SVC()
    svm_model.fit(X, y)
    data_dict['final_svm_model'] = svm_model
    # Save the updated model dictionary
    with open('new_disease_prediction_system.pkl', 'wb') as file:
        pickle.dump(data_dict, file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/inner')
def inner():
    return render_template('inner.html', symptoms=symptoms)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        selected_symptoms = []
        
        # Check if we're using checkbox or manual entry
        if 'symptoms' in request.form:
            # Get symptoms from checkboxes
            selected_symptoms = request.form.getlist('symptoms')
        elif 'manual_symptoms' in request.form:
            # Get symptoms from manual entry
            manual_input = request.form.get('manual_symptoms', '').strip()
            if manual_input:
                # Split by commas and clean up each symptom
                manual_symptoms = [s.strip().lower() for s in manual_input.split(',')]
                
                # Try to match manual symptoms with our symptom list
                for manual_symptom in manual_symptoms:
                    # Find the closest match in our symptom list
                    matched = False
                    for db_symptom in symptoms:
                        if manual_symptom in db_symptom.lower() or db_symptom.lower().replace('_', ' ') in manual_symptom:
                            selected_symptoms.append(db_symptom)
                            matched = True
                            break
                    
                    # If no match found, use exact match if it exists
                    if not matched and manual_symptom in symptoms:
                        selected_symptoms.append(manual_symptom)
        
        # Create input data for the models
        input_data = np.zeros(len(symptoms))
        for symptom in selected_symptoms:
            if symptom in symptoms:
                input_data[symptoms.index(symptom)] = 1
        
        input_data = input_data.reshape(1, -1)
        
        # Make predictions with all three models
        rf_disease = data_dict["final_rf_model"].predict(input_data)[0]
        nb_disease = data_dict["final_nb_model"].predict(input_data)[0]
        svm_disease = data_dict["final_svm_model"].predict(input_data)[0]
        
        # Get the final prediction through majority voting
        predictions = [rf_disease, nb_disease, svm_disease]
        prediction_counts = Counter(predictions)
        final_disease = prediction_counts.most_common(1)[0][0]
        
        # Calculate confidence percentage based on agreement
        max_count = prediction_counts[final_disease]
        confidence = int((max_count / len(predictions)) * 100)
        
        # Format selected symptoms for display
        display_symptoms = [symptom.replace('_', ' ').title() for symptom in selected_symptoms]
        
        result = {
            "rf_model_prediction": rf_disease,
            "naive_bayes_prediction": nb_disease,
            "svm_model_prediction": svm_disease,
            "final_prediction": final_disease,
            "confidence": confidence,
            "symptoms": display_symptoms
        }
        
        return render_template('result.html', result=result)
    
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        return jsonify({"error": str(e), "traceback": error_trace})

if __name__ == '__main__':
    app.run(debug=True) 