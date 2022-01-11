# Import Libraries
from __future__ import print_function
import os
import sys
from pycaret.classification import *
import pandas as pd
from flask import Flask, render_template, request


model=load_model('model')


app = Flask(__name__)

@app.route('/')
def entry_page():
    # Nicepage template of the webpage
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def render_message():
    try:
        # Get data input
        Age	= float(request.form['age'])
        SystolicBP= float(request.form['sbp'])
        DiastolicBP	= float(request.form['dbp'])
        BS = float(request.form['bs'])
        BodyTemp = float(request.form['bt'])
        HeartRate = float(request.form['hr'])

        data = [[Age, SystolicBP,	DiastolicBP, BS, BodyTemp, HeartRate]]
        cols = ['Age', 'SystolicBP', 'DiastolicBP', 'BS', 'BodyTemp', 'HeartRate']

        data_unseen = pd.DataFrame(data, columns = cols)        
        prediction= predict_model(model, data=data_unseen, round = 0)
        preds= prediction.Label[0]
        print(preds, file=sys.stderr)
        
        print('Python module executed successfully')
        message = 'Risk Level : {} !'.format(preds.split(' ', 1)[0].title())
        # print(message, file=sys.stderr)
    except Exception as e:
        # Store error to pass to the web page
        message = "Error encountered. Try with other values. ErrorClass: {}, Argument: {} and Traceback details are: {}".format(
            e.__class__, e.args, e.__doc__)
    # Return the model results to the web page
    return render_template('index.html' ,message=message)

if __name__ == '__main__':
    # app.run(debug=True , host='localhost', port=8080)
    app.run(host="0.0.0.0", port=8080)
