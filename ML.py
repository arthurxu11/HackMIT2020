import json, time, shutil
from ibm_watson import VisualRecognitionV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from flask import Flask, render_template, request
from PIL import Image
import numpy as np
import cv2

# IBM Watson Auth
authenticator = IAMAuthenticator('3gA07UmUh08PnJgMhVJ4dMfrzCXPnzerpHaTo32UNRvT')
visual_recognition = VisualRecognitionV3(version='2018-03-19', authenticator=authenticator)
visual_recognition.set_service_url('https://api.us-south.visual-recognition.watson.cloud.ibm.com/instances/3d2b99fc-1cc4-4049-a15e-90501534d482')

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def home():
    return "<h1>Hello World</p>"

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return '<h1>Login here</h1>'

@app.route('/add', methods=['POST'])
def add():
    imagefile = request.files
    print(type(imagefile))
    for x in range(1, 11):
        print(x)
        name = "Card" + str(time.time())+str(x)+".jpg"
        im1 = imagefile.save(name)
        shutil.move(name, "./images")
    return "Beans"

@app.route('/loggedin')
def loggedin():
    return '<h1>Welcome</h1>'
# with open('./beagle.zip', 'rb') as beagle, open(
#         './golden-retriever.zip', 'rb') as goldenretriever, open(
#             './husky.zip', 'rb') as husky, open(
#                 './cats.zip', 'rb') as cats:
#     model = visual_recognition.create_classifier(
#         'dogs',
#         positive_examples={'beagle': beagle, 'goldenretriever': goldenretriever, 'husky': husky},
#         negative_examples=cats).get_result()
# print(json.dumps(model, indent=2))

app.run(debug=True)