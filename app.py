from flask import Flask,render_template, url_for,redirect,request,flash,send_from_directory
import numpy as np
from PIL import ImageGrab, Image
import os
from tensorflow import keras
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename
import win32gui

app = Flask(__name__, static_folder='static', template_folder='templates')

dir_path = os.path.dirname(os.path.realpath(__file__))
# UPLOAD_FOLDER = dir_path + '/uploads'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


#HdwD model read
model = load_model('HandWrittenDigit/mnist.h5')

def predict_digit(full_path):
    data = image.load_img(full_path, target_size=(28,28))
    data = data.convert('L')#convert rgb to grayscale
    data = np.array(data)
    data = data.reshape([1,28,28,1],order='C')#reshaping to support our model input and normalizing
    data = data/255.0
    res = model.predict([data])[0]#predicting the class
    return np.argmax(res), max(res)


@app.route('/')
def index():
	return render_template('home.html')

@app.route('/home')
def home():
	return render_template('home.html')
    
@app.route('/hwdrpredict', methods=['GET','POST'])
def hwdrpredict():
    if request.method == 'POST':

        file = request.files['image']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for("corona"))
        if file:
            full_name = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(full_name)

        digit, acc = predict_digit(full_name)

        return render_template('hwdrshow.html',image_file_name = file.filename,text= str(digit),proba=str(int(acc*100)))
    return render_template('hwdr.html')

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

        
if __name__ == '__main__':
	app.run(debug=True)

