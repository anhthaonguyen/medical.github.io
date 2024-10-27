#importing Necessary Libraries

import numpy as np
import pandas as pd
import pickle as pkl 
import streamlit as st


model = pkl.load(open('MIPML.PKL', 'rb'))

# Thiết lập giao diện Streamlit:
st.header('Medical Insurance Premium Predictor')

# Input fields for the user-Xử lý đầu vào:
gender = st.selectbox('Choose Gender', ['Female', 'Male'])
smoker = st.selectbox('Are you a smoker?', ['Yes', 'No'])
region = st.selectbox('Choose Region', ['SouthEast', 'SouthWest', 'NorthEast', 'NorthWest'])
age = st.slider('Enter Age', 5, 80)
bmi = st.number_input('Enter BMI', min_value=5.0, max_value=100.0, value=25.0, step=0.1)
children = st.slider('Choose No of Children', 0, 5)

# Llogic xử lý khi người dùng nhấn nút Predict
if st.button('Predict'):
    # Xử lý biến đầu vào
    gender = 0 if gender == 'Female' else 1
    smoker = 1 if smoker == 'Yes' else 0
    # Mã hóa biến vùng miền
    if region == 'SouthEast':
        SouthEast, SouthWest, NorthEast, NorthWest = 1, 0, 0, 0
    elif region == 'SouthWest':
        SouthEast, SouthWest, NorthEast, NorthWest = 0, 1, 0, 0
    elif region == 'NorthEast':
        SouthEast, SouthWest, NorthEast, NorthWest = 0, 0, 1, 0
    else:  # NorthWest
        SouthEast, SouthWest, NorthEast, NorthWest = 0, 0, 0, 1
    # Chuẩn bị dữ liệu đầu vào cho mô hình:
    from sklearn.preprocessing import StandardScaler
    input_data = (age, gender, bmi, children, smoker, SouthEast, SouthWest, NorthEast, NorthWest)
    input_data_array = np.asarray(input_data).reshape(1, -1)
    predicted_prem_log = model.predict(input_data_array)
    insurance_premium = np.exp(predicted_prem_log) - 1
    display_string = 'Insurance Premium will be '+ str(round(insurance_premium[0],2)) + ' USD Dollars'
    st.markdown(display_string)

