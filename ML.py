import json, time, shutil, cv2, io, os, math, shutil
from ibm_watson import VisualRecognitionV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from flask import Flask, render_template, request, redirect, session, url_for, make_response, jsonify
from flask_session import Session
from flask_cors import CORS
from PIL import Image
import numpy as np

# IBM Watson Auth
authenticator = IAMAuthenticator('3gA07UmUh08PnJgMhVJ4dMfrzCXPnzerpHaTo32UNRvT')
visual_recognition = VisualRecognitionV3(version='2018-03-19', authenticator=authenticator)
visual_recognition.set_service_url('https://api.us-south.visual-recognition.watson.cloud.ibm.com/instances/3d2b99fc-1cc4-4049-a15e-90501534d482')

app = Flask(__name__)
# app.config["DEBUG"] = True
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG"]
app.config["IMAGE_UPLOADS"] = './images'
# app.config['SECRET_KEY'] = b'abcd123'
app.secret_key = b'abcd123'
# Session(app)
CORS(app)

@app.route('/')
def home():
    print(session.get("guess"))
    return "<h1>Hello World</p>"

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/add', methods=['POST'])
def add():
    if request.method == "POST":
        if request.files:
            name = request.form['name'].replace(" ", "_")
            name2 = request.form['name']
            userfolder = str(name)+"images"
            print(userfolder)
            path = os.path.join("./images", userfolder)
            os.mkdir(path)
            uploaded_files = request.files.getlist("file[]")
            count = 0
            times = math.ceil(10/len(uploaded_files))
            for image in uploaded_files:  # image will be the key
                for x in range(0, times):
                    photoname = "./images/"+userfolder+"/"+userfolder+str(count)+".jpeg"
                    im1 = image.save(photoname)
                    count += 1
            shutil.make_archive(userfolder, 'zip', "./images/"+userfolder)
            shutil.move(userfolder+".zip", "./images/"+userfolder)
            with open("./images/"+userfolder+"/"+userfolder+".zip", 'rb') as card:
                updated_model = visual_recognition.update_classifier(classifier_id='cards_176556607', positive_examples={name2: card}).get_result()
            print(json.dumps(updated_model, indent=2))

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

@app.route('/check', methods=["POST", "GET"])
def check():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            name = image.filename[:-4]+str(time.time())+".jpg"
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], name))
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
                os.remove(images_file)
            name = topguess
            name.replace(" ", "_")
            data = {'name': name, "confidence": max}
            return jsonify(data)

@app.route('/statuscheck', methods=["GET"])
def statuscheck():
    return render_template("status.html")

@app.route('/status', methods=["POST"])
def status():
    content = request.json
    name = content['name']
    classifier = visual_recognition.get_classifier(classifier_id='cards_176556607').get_result()
    status = classifier['status']
    print(status)

@app.route('/loggedin/<usr>/<score>')
def loggedin(usr, score):
    print(usr, score)
    usr = usr.replace("_", " ")
    # print(session['guess'])
    # if "data" in session:
    # topguess = json.loads(session['data'])
    return render_template("loggedin.html", messages=[usr, score])
    # else:
    #     return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
