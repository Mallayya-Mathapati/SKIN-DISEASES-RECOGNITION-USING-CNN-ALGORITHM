from flask import Flask, render_template, request
import keras
from keras.models import load_model
from keras.preprocessing import image
import tensorflow as tf
from tensorflow.keras import models, layers
import numpy as np
from datetime import date

app = Flask(__name__)

class_names = {0 : 'Acne and Rosacea', 1 : 'Atopic Dermatitis',2:'Bullous Disease',3:'Eczema',4:'Light Diseases and Disorders of Pigmentation',5:'Lupus and other Connective Tissue diseases',6:'Nail Fungus and other Nail Disease',7:'Psoriasis pictures Lichen Planus and related diseases',8:'Seborrheic Keratoses and other Benign Tumors',9:'Tinea Ringworm Candidiasis and other Fungal Infections',10:'Urticaria Hives',11:'Vasculitis',12:'Warts Molluscum and other Viral Infections'}
#class_names={0 :"Acne and Rosacea",1:"Nail Fungus",2:"Tinea Ringworm"}
user_history_data=[["Name","Age","sex","date","skin diseases"]]

model = keras.models.load_model('models/keras_model.h5')

model.make_predict_function()

def predict_label(img_path):
	#i = image.load_img(img_path, target_size=(100,100))
	#i = image.img_to_array(i)/255.0
	#i = i.reshape(1, 200,200,3)
	#p = model.predict(i)

	img_array = image.load_img(img_path, target_size=(224,224))
	img_array= image.img_to_array(img_array)/255.0
	img_array= img_array.reshape(1, 224,224,3)
	predictions = model.predict(img_array)
	predicted_class = class_names[np.argmax(predictions[0])]
	confidence = round(100 * (np.max(predictions[0])),2)

	return str(predicted_class)#"Predicated class:"+str(predicted_class)+" ,confidence:"+str(confidence)


# routes
@app.route("/", methods=['GET', 'POST'])
def main():
	return render_template("index.html")

@app.route("/how_to_use")
def how_to_use():
	return render_template("how_to_use.html")

@app.route("/welcome")
def welcome():
	return render_template("welcome.html")

@app.route("/our_services")
def our_services():
	return render_template("our_services.html")

@app.route("/dashboard")
def dashboard():
	return render_template("dashboard.html")

@app.route("/get_report")
def get_report():
	return render_template("get_report.html")

@app.route("/about")
def about_page():
	return "Please subscribe  Artificial Intelligence Hub..!!!"

@app.route("/report_card", methods = ['GET', 'POST'])
def get_op():
	global user_history_data
	if request.method == 'POST':
		img = request.files['upload_img']
		#name=request.form.get['name']
		#age=request.form.get['age']
		#sex=request.form.get['gender']
		#today=date.today()
		img_path = "static/images" + img.filename	
		img.save(img_path)
		p= predict_label(img_path)
		#diseases=P
		#user_data=[name,age,sex,today,diseases]
		#user_history_data.append([name,age,sex,today,diseases])
		#print(user_data)

		return render_template("report_card.html", prediction = p, img_path = img_path)

@app.route("/table", methods = ['GET', 'POST'])
def user_his():
	if request.method == 'POST':
		img = request.files['upload_img']
		name=request.form.get['name']
		age=request.form.get['age']
		sex=request.form.get['gender']
		today=date.today()
		img_path = "static/images" + img.filename	
		img.save(img_path)
		p = predict_label(img_path)
		diseases=P
		user_data=[name,age,sex,today,diseases]
		user_history_data.append([name,age,sex,today,diseases])
		print(user_data)
	return render_template("table.html", prediction = p, img_path = img_path,data=user_data)

def get_output():
	global user_history_data
	if request.method == 'POST':
		img = request.files['upload_img']
		name=request.form.get['name']
		age=request.form.get['age']
		sex=request.form.get['gender']
		today=date.today()
		
		img_path = "static/" + img.filename	
		img.save(img_path)

		p = predict_label(img_path)
		diseases=P
		user_data=[name,age,sex,today,diseases]

		user_history_data.append([name,age,sex,today,diseases])

	return render_template("report_card.html", prediction = p, img_path = img_path,data=user_data)

if __name__ =='__main__':
	#app.debug = True
	app.run(debug = True)
