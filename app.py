from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn

app = Flask(__name__)


with open('random_forest_classifier','rb') as f:
   mp = pickle.load(f)
    
with open('standard_scaler','rb') as f:
    ss = pickle.load(f)

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')

 
@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        age = float(request.form['age'])
        creatinine_phosphokinase = int(request.form['creatinine_phosphokinase'])
        ejection_fraction = int(request.form['ejection_fraction'])
        platelets = float(request.form['platelets'])
        serum_creatinine = float(request.form['serum_creatinine'])
        serum_sodium = int(request.form['serum_sodium'])
       
        anaemia = request.form['anaemia']
        if (anaemia=='Yes'):
           anaemia=1
        else:
           anaemia=0
           
        diabetes = request.form['diabetes']
        if (diabetes=='Yes'):
           diabetes=1
        else:
           diabetes=0
           
        high_blood_pressure = request.form['high_blood_pressure']
        if (high_blood_pressure=='Yes'):
           high_blood_pressure=1
        else:
           high_blood_pressure=0
           
        sex = request.form['sex']
        if (sex=='Male'):
           sex=1
        else:
           sex=0
           
        smoking = request.form['smoke']
        if (smoking=='Yes'):
          smoking=1
        else:
          smoking=0    
 
        array = np.array([age,anaemia,creatinine_phosphokinase,diabetes,ejection_fraction,high_blood_pressure,platelets,serum_creatinine,serum_sodium,sex,smoking])    
        array = array.reshape(1,-1)
        transformed_array = ss.transform(array)
        prediction = mp.predict(transformed_array)
        output = prediction[0]
        
        if (output==1):
          return render_template('index.html',prediction_texts='You are likely to have a fatal heart attack')
        elif (output==0):
          return render_template('index.html',prediction_texts='You are not likely to have a fatal heart attack')
        else:
          return render_template('index.html')

if __name__=="__main__":
 app.run(debug=True)