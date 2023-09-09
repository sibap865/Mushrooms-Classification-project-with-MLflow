from flask import Flask, render_template, request
import os 
import numpy as np
import pandas as pd
from MushroomProject.pipeline.prediction import PredictionPipeline

app = Flask(__name__) # initializing a flask app

@app.route('/',methods=['GET'])  # route to display the home page
def homePage():
    return render_template("index.html")


@app.route('/train',methods=['GET'])  # route to train the pipeline
def training():
    os.system("python main.py")
    return "Training Successful!" 


@app.route('/predict',methods=['POST','GET']) # route to show the predictions in a web UI
def index():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            cap_shape =int(request.form['cap_shape'])
            cap_surface =int(request.form['cap_surface'])
            cap_color =int(request.form['cap_color'])
            bruises =int(request.form['bruises'])
            odor =int(request.form['odor'])
            gill_attachment =int(request.form['gill_attachment'])
            gill_spacing =int(request.form['gill_spacing'])
            gill_size =int(request.form['gill_size'])
            gill_color =int(request.form['gill_color'])
            stalk_shape =int(request.form['stalk_shape'])
            stalk_surface_above_ring =int(request.form['stalk_surface_above_ring'])
            stalk_surface_below_ring =int(request.form['stalk_surface_below_ring'])
            stalk_color_above_ring =int(request.form['stalk_color_above_ring'])
            stalk_color_below_ring =int(request.form['stalk_color_below_ring'])
            veil_color =int(request.form['veil_color'])
            ring_number =int(request.form['ring_number'])
            ring_type =int(request.form['ring_type'])
            spore_print_color =int(request.form['spore_print_color'])
            population =int(request.form['population'])
            habitat =int(request.form['habitat'])


            
       
         
            data = [cap_shape,cap_surface,cap_color,bruises,odor,gill_attachment,gill_spacing,gill_size,gill_color,stalk_shape,stalk_surface_above_ring,stalk_surface_below_ring,stalk_color_above_ring,stalk_color_below_ring,veil_color,ring_number,ring_type,spore_print_color,population,habitat]
            data = np.array(data).reshape(1, 20)
            
            obj = PredictionPipeline()
            predict = obj.predict(data)
            result ={0:"edible",1:"poisonous"}
            return render_template('results.html', prediction = str(result[predict]))

        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'

    else:
        return render_template('index.html')


if __name__ == "__main__":
	# app.run(host="0.0.0.0", port = 8080, debug=True)
	app.run(host="0.0.0.0", port = 8080)