import json, time, shutil
from ibm_watson import VisualRecognitionV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from flask import Flask, render_template, request, redirect, session, url_for
from PIL import Image
import numpy as np
import cv2, io, os
from werkzeug.utils import secure_filename

# IBM Watson Auth
authenticator = IAMAuthenticator('3gA07UmUh08PnJgMhVJ4dMfrzCXPnzerpHaTo32UNRvT')
visual_recognition = VisualRecognitionV3(version='2018-03-19', authenticator=authenticator)
visual_recognition.set_service_url('https://api.us-south.visual-recognition.watson.cloud.ibm.com/instances/3d2b99fc-1cc4-4049-a15e-90501534d482')

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG"]
app.config["IMAGE_UPLOADS"] = './images'
app.config['SECRET_KEY'] = 'Test123'

@app.route('/')
def home():
    return "<h1>Hello World</p>"

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/add', methods=['POST'])
def add():
    print(request.files)
    if request.method == 'POST' and 'photo' in request.files:
        print("Test")
        photo = request.files['photo']
        in_memory_file = io.BytesIO()
        photo.save(in_memory_file)
        data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
        color_image_flag = 1
        img = cv2.imdecode(data, color_image_flag)
        im1 = img.save("Test.jpg")

    # imagefile = request.files
    # print(type(imagefile))
    # for x in range(1, 11):
    #     print(x)
    #     name = "Card" + str(time.time())+str(x)+".jpg"
    #     im1 = imagefile.save(name)
    #     shutil.move(name, "./images")
    # return "Beans"

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/check', methods=["POST"])
def check():
    if request.method == "POST":

        if request.files:
            image = request.files["image"]

            name = image.filename[:-4]+str(time.time())+".jpg"
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], name))
            print("2")
            with open("./images/"+name, 'rb') as images_file:
                classes = visual_recognition.classify(images_file=images_file, classifier_ids=['cards_176556607']).get_result()
                guesses = classes['images'][0]['classifiers'][0]['classes']
                max = 0
                topguess = ""
                for x in guesses:
                    guess = x['class']
                    score = x['score']
                    if score > max:
                        topguess = guess
                        max = score

    # messages = json.dumps({"topguess": topguess, "confidence": str(score)})
    # session['messages'] = messages
    messages = [topguess, max]
    # return redirect(url_for('loggedin', messages=[topguess, max]))
    return render_template("loggedin.html", messages=messages)

@app.route('/loggedin')
def loggedin(messages):
    # messages = request.args['messages']  # counterpart for url_for()
    # messages = session['messages']
    # print(messages)# counterpart for session
    return render_template("loggedin.html", messages=messages)
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