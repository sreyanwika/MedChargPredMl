import json
import pickle

from flask import Flask,request,app,jsonify,url_for,render_template
import numpy as np
import pandas as pd

app=Flask(__name__)
## Load the model

regmodel=pickle.load(open('XGBregmodel.pkl','rb'))
#scalar=pickle.load(open('scaling.pkl','rb'))
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict_api',methods=['POST'])
def predict_api():
    data=pd.DataFrame(request.json['data'], index=[0])
    print(data)
    data['smoker']=data['smoker'].map({'yes':1,'no':0})
    print(data.to_numpy())
    #new_data=scalar.transform(np.array(list(data.values())).reshape(1,-1))
    new_data=data.to_numpy()
    #new_data=data
    output=regmodel.predict(new_data)
    print(output[0])
    return jsonify(str(output[0]))

@app.route('/predict',methods=['POST'])
def predict():
    data=pd.DataFrame([float(x) for x in request.form.values()])
    #data=pd.DataFrame(request.form.values(),index=[0])
    #data['SMOKE']=data['SMOKE'].map({'yes':1,'no':0})
    final_input=np.array(data).reshape(1,-1)
    #final_input=data.to_numpy()
    print(final_input)
    output=regmodel.predict(final_input)[0]
    return render_template("home.html",prediction_text="The medical charges price prediction is {}".format(output))



if __name__=="__main__":
    app.run(debug=True)
   
     