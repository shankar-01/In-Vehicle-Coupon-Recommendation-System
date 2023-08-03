
from flask import Flask, request, jsonify, render_template, send_file
import joblib
import numpy as np
app = Flask(__name__)
# prediction function
def Predict(to_predict_list):
	to_predict = np.array(to_predict_list).reshape(1, len(to_predict_list))
	loaded_model = joblib.load(open("InVehicleCouponRecommendationPredictor.pkl", "rb"))
	result = loaded_model.predict(to_predict)
	return result[0]

def convertData(dict):
	features = ['direction_same', 'destination',
       'destination', 'passanger', 'weather', 'time', 'coupon', 'expiration_2h', 'gender_Male',
       'education', 'coupoun']
	print(dict)
	for x in features:
		if not x in dict.keys() or dict[x] == '':
			print("n k ", x)
			dict[x] = 0
	myList = []
	myList.append(dict['direction_same'])
	if dict["destination"] == "_No Urgent Place":
		myList.append(1)
	else:
		myList.append(0)
	if dict["destination"] == "_Work":
		myList.append(1)
	else:
		myList.append(0)
	
	if dict["passanger"] == "_Friends(s)":
		myList.append(1)
	else:
		myList.append(0)
	if dict["passanger"] == "_Kid(s)":
		myList.append(1)
	else:
		myList.append(0)
	if dict["passanger"] == "_Partner":
		myList.append(1)
	else:
		myList.append(0)
	
	if dict["weather"] == "_Snowy":
		myList.append(1)
	else:
		myList.append(0)
	if dict["weather"] == "_Sunny":
		myList.append(1)
	else:
		myList.append(0)

	
	if dict["time"] == '_10PM':
		myList.append(1)
	else:
		myList.append(0)
	if dict["time"] == '_2PM':
		myList.append(1)
	else:
		myList.append(0)
	if dict["time"] == '_6PM':
		myList.append(1)
	else:
		myList.append(0)
	if dict["time"] == '_7AM':
		myList.append(1)
	else:
		myList.append(0)
	if dict['coupon'] == '_Carry out & Take away':
		myList.append(1)
	else:
		myList.append(0)
	if dict['coupon'] == '_Coffee House':
		myList.append(1)
	else:
		myList.append(0)
	if dict['coupon'] == '_Restaurant(20,50)':
		myList.append(1)
	else:
		myList.append(0)
	if dict['coupon'] == '_Restaurant(20)':
		myList.append(1)
	else:
		myList.append(0)
	myList.append(dict['expiration_2h'])
	myList.append(dict['gender_Male'])
	
	if dict['education'] == '_Bachelors degree':
		myList.append(1)
	else:
		myList.append(0)
	if dict['education'] == '_Graduate degree (Masters or Doctorate)':
		myList.append(1)
	else:
		myList.append(0)
	if dict['education'] == '_High School Graduate':
		myList.append(1)
	else:
		myList.append(0)
	if dict['education'] == '_Some High School':
		myList.append(1)
	else:
		myList.append(0)
	if dict['education'] == '_Some college - no degree':
		myList.append(1)
	else:
		myList.append(0)

	if dict["coupon_freq"] == '_4~8':
		myList.append(1)
	else:
		myList.append(0)
	if dict["coupon_freq"] == '_gt8':
		myList.append(1)
	else:
		myList.append(0)
	if dict["coupon_freq"] == '_less1':
		myList.append(1)
	else:
		myList.append(0)
	if dict["coupon_freq"] == '_never':
		myList.append(1)
	else:
		myList.append(0)
	myList = [int(x) for x in myList]
	return myList
	
@app.route('/')
def home():
	return render_template("index.html")
@app.route('/projectdetails')
def projectdetails():
	return render_template("projectdetails.html")
@app.route('/downloadReport')
def downloadReport():
	return send_file('report.pdf')
@app.route('/result', methods = ['POST'])
def result():
	if request.method == 'POST':
		to_predict_list = request.form.to_dict()
		#to_predict_list = list(to_predict_list.values())
		#to_predict_list = list(map(int, to_predict_list))
			
		inputV = list(map(int, convertData(to_predict_list)))
		result = Predict(inputV)
		print(inputV)
		

		if int(result)== 1:
			prediction ='accept the coupon'
		else:
			prediction ='not accept the coupon'
		
		return jsonify(alert=prediction)
