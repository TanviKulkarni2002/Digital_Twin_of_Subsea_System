from flask import Flask, render_template, send_from_directory,request, jsonify,request
import pickle
import numpy as np
# from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures
import pandas as pd

app = Flask(__name__)

d_air=0
d_temp=0
d_pres=0
#'rpm', 'motor_power', 'torque', 'outlet_pressure_bar', 'air_flow', 'noise_db', 'outlet_temp', 'wpump_outlet_press', 'water_inlet_temp',        'water_outlet_temp', 'wpump_power', 'water_flow', 'oil_tank_temp', 'bearings', 'wpump', 'radiator', 'exvalve'
# features = np.array([499,1405.843,27.51171,40.84052,2.960632,43.16639,47.25294,216.6105,59.0806,45.80618,0,0,0,0])
# Load the trained model
with open('model/ML Model/airflow_model.pkl', 'rb') as file:
    air_flow = pickle.load(file)

with open('model/ML Model/outlet_pres_model.pkl', 'rb') as file:
    out_pres = pickle.load(file)

with open('model/ML Model/outlet_temp_model.pkl', 'rb') as file:
    out_temp = pickle.load(file)
    
# with open('model/ML Model/scaler_air.pkl', 'rb') as file:
#     scaler_air = pickle.load(file)

# with open('model/ML Model/scaler_temp.pkl', 'rb') as file:
#     scaler_temp = pickle.load(file)
   
# with open('model/ML Model/scaler_pres.pkl', 'rb') as file:
#     scaler_pres = pickle.load(file)

# scaling_params = np.load('model/ML Model/scaling_params.npz')
# mean = scaling_params['mean']
# std_dev = scaling_params['std_dev']

# scaling_params1 = np.load('model/ML Model/scaling_params_air.npz')
# air_mean = scaling_params1['mean']
# air_std_dev = scaling_params1['std_dev']

# scaling_params2 = np.load('model/ML Model/scaling_params_temp.npz')
# temp_mean = scaling_params2['mean']
# temp_std_dev = scaling_params2['std_dev']

# scaling_params3 = np.load('model/ML Model/scaling_params_pres.npz')
# pres_mean = scaling_params3['mean']
# pres_std_dev = scaling_params3['std_dev']

# app = Flask(name)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/model/<path:path>')
def send_model(path):
    return send_from_directory('model', path)


@app.route('/predict', methods=['POST','GET'])
def predict():
    # Get the input data from the request
    global d_air, d_temp, d_pres
    print("entered")
    input_file = request.files['inputFile']
    df = pd.read_csv(input_file)
    print(df)
    input = df.iloc[0].values.reshape(1, -1)  # Reshape to a 2D array
    print(input)
    poly_reg = PolynomialFeatures(degree=2,include_bias=False)
    final_input = poly_reg.fit_transform(input)
    d_air = air_flow.predict(final_input).tolist()
    d_temp = out_temp.predict(final_input).tolist()
    d_pres = out_pres.predict(final_input).tolist()
    print(d_air,d_temp,d_pres)
    return jsonify({'air': d_air,'temp':d_temp,'pressure':d_pres})    

# @app.route('/air_flow', methods=['POST','GET'])
# def predict_air():
#    global d_air, d_temp, d_pres, features
#    features_air = np.insert(features, 3, d_pres)
#    features_air = np.insert(features_air, 6, d_temp)
#    #scaler = StandardScaler()
# #    scaled_data = scaler_air.fit_transform(features_air.reshape(1,-1))
# #    mean_values = scaler_air.mean_
# #    std_dev_values = scaler_air.scale_
# #    print("airflow scale:",mean_values,"and",std_dev_values)
#    scaled_data=(features_air - mean) / std_dev
#    cols = ['rpm', 'motor_power', 'torque', 'outlet_pressure_bar', 'noise_db', 'outlet_temp', 'wpump_outlet_press',  'water_inlet_temp', 'water_outlet_temp', 'wpump_power', 'water_flow', 'oil_tank_temp', 'bearings', 'wpump', 'radiator', 'exvalve']
#    new_data = pd.DataFrame(scaled_data.reshape(1,-1), columns=cols)
#    poly_reg = PolynomialFeatures(degree=2,include_bias=False)
#    d = poly_reg.fit_transform(new_data)
#    scaled_pred = air_flow.predict(d)
#    air_orig_pred = ((scaled_pred * air_std_dev) + air_mean)
#    print('prediction-airflow: ', (air_orig_pred))
#    return jsonify({'prediction': air_orig_pred.tolist()})

# @app.route('/out_temp', methods=['POST','GET'])
# def predict_temp():
#    global d_air, d_temp, d_pres, features
#    features_temp = np.insert(features, 3, d_pres)
#    features_temp = np.insert(features_temp, 4, d_air)
#    #scaler = StandardScaler()
#    scaled_data=(features_temp - mean) / std_dev
#    cols = ['rpm', 'motor_power', 'torque', 'outlet_pressure_bar', 'noise_db', 'outlet_temp', 'wpump_outlet_press',  'water_inlet_temp', 'water_outlet_temp', 'wpump_power', 'water_flow', 'oil_tank_temp', 'bearings', 'wpump', 'radiator', 'exvalve']
#    new_data = pd.DataFrame(scaled_data.reshape(1,-1), columns=cols)
#    poly_reg = PolynomialFeatures(degree=2,include_bias=False)
#    d = poly_reg.fit_transform(new_data)
#    scaled_pred = air_flow.predict(d)
#    temp_orig_pred = (scaled_pred * temp_std_dev) + temp_mean
#    print('prediction-temp: ', temp_orig_pred)
#    return jsonify({'prediction': temp_orig_pred.tolist()})

# @app.route('/out_pres', methods=['POST','GET'])
# def predict_pres():
#    global d_air, d_temp, d_pres, features
#    features_pres = np.insert(features, 4, d_air)
#    features_pres = np.insert(features_pres, 6, d_temp)
#    #scaler = StandardScaler()
#    scaled_data=(features_pres - mean) / std_dev
#    cols = ['rpm', 'motor_power', 'torque', 'outlet_pressure_bar', 'noise_db', 'outlet_temp', 'wpump_outlet_press',  'water_inlet_temp', 'water_outlet_temp', 'wpump_power', 'water_flow', 'oil_tank_temp', 'bearings', 'wpump', 'radiator', 'exvalve']
#    new_data = pd.DataFrame(scaled_data.reshape(1,-1), columns=cols)
#    poly_reg = PolynomialFeatures(degree=2,include_bias=False)
#    d = poly_reg.fit_transform(new_data)
#    scaled_pred = air_flow.predict(d)
#    pres_orig_pred = (scaled_pred * pres_std_dev) + pres_mean
#    print('prediction-pressure: ', pres_orig_pred)
#    return jsonify({'prediction': pres_orig_pred.tolist()})       
   

if __name__ == '__main__':
    app.run(debug=True)