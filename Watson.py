import json
from ibm_watson import VisualRecognitionV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# IBM Watson Auth
authenticator = IAMAuthenticator('P27A7uRN6YOLCrpxpBhQMrWz0Xhk-RWdhzO0LVcmKY6g')
visual_recognition = VisualRecognitionV3(version='2018-03-19', authenticator=authenticator)
visual_recognition.set_service_url('https://api.us-south.visual-recognition.watson.cloud.ibm.com/instances/c436bb25-90e3-40fa-adfa-ebcbc5226a13')

with open('./Card Photos/2019.zip', 'rb') as nineteen, open('./Card Photos/2020.zip', 'rb') as twenty, open('./Card Photos/Penn.zip', 'rb') as penn, open('./Card Photos/YMCA.zip', 'rb') as ymca:
    model = visual_recognition.create_classifier('mycards',positive_examples={'Arthur 2019': nineteen, 'Arthur 2020': twenty, 'Arthur Penn': penn, "Arthur YMCA": ymca}).get_result()
print(json.dumps(model, indent=2))

# classifier = visual_recognition.get_classifier(classifier_id='cards_176556607').get_result()
# print(json.dumps(classifier, indent=2))