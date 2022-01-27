import urllib.request
import json
import os
import ssl

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

# Request data goes here
data = {
    "Inputs": {
        "data":
        [
            {
                'Pregnancies': "0",
                'Glucose': "0",
                'BloodPressure': "0",
                'SkinThickness': "0",
                'Insulin': "0",
                'BMI': "0",
                'DiabetesPedigreeFunction': "0",
                'Age': "0",
            },
        ],
    },
    "GlobalParameters": {
        'method': "predict",
    }
}

body = str.encode(json.dumps(data))

url = 'http://a33270bf-302e-40ba-bfca-c3149553b944.southeastasia.azurecontainer.io/score'
api_key = '8jJ7pTvHeP1PkxubrgadxuIWCnFHJ7vw' # Replace this with the API key for the web service
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)

    result = response.read()
    print(result)
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(json.loads(error.read().decode("utf8", 'ignore')))