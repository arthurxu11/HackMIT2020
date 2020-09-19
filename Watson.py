import json
from ibm_watson import VisualRecognitionV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# IBM Watson Auth
authenticator = IAMAuthenticator('3gA07UmUh08PnJgMhVJ4dMfrzCXPnzerpHaTo32UNRvT')
visual_recognition = VisualRecognitionV3(version='2018-03-19', authenticator=authenticator)
visual_recognition.set_service_url('https://api.us-south.visual-recognition.watson.cloud.ibm.com/instances/3d2b99fc-1cc4-4049-a15e-90501534d482')

# with open('./images1.zip', 'rb') as images1, open('./images2.zip', 'rb') as images2:
#     model = visual_recognition.create_classifier('cards',positive_examples={'arthurxu1': images1, 'arthurxu2': images2},).get_result()
# print(json.dumps(model, indent=2))

classifier = visual_recognition.get_classifier(classifier_id='cards_176556607').get_result()
print(json.dumps(classifier, indent=2))