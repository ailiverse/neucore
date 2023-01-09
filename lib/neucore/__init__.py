from tqdm import tqdm

import requests
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

import json
import base64
import time
from pathlib import Path

from .env import URL_DICT, SIGN_IN_URL, SIGN_UP_URL

from .uploadUtils import upload_in_chunks, IterableToFileAdapter

def signUp(email, password, confirm_password, organization):
    data =  { "email": email,
              "password": password,
              "confirm_password": confirm_password,
              "organization": organization}
  
    response = requests.post(SIGN_UP_URL, data=json.dumps(data), headers={"Content-type": "application/json"})
    response_json = response.json()
    if "authToken" not in response_json:
        raise Exception(response_json)

    return response_json['authToken']

def signIn(email, password):
    data =  { "email": email,
              "password": password}

    response = requests.post(SIGN_IN_URL, data=json.dumps(data), headers={"Content-type": "application/json"})
    response_json = response.json()
    if "authToken" not in response_json:
        raise Exception(response_json)
    
    return response_json['authToken']


class Model:
    def __init__(self, authToken, modelID=None, model=None, version="1"):
        self.authToken = authToken
        self.version = version
        # create a new model if modelID is not specified
        if modelID is None and model is None:
            raise Exception("Please specify either modelID or model")
        elif modelID is None:
            modelID = self.createModel(authToken, model)
        self.modelID = modelID


    def createModel(self, authToken, model):
        CREATE_MODEL_URL = URL_DICT[self.version]["CREATE_MODEL_URL"]
        data =  { "model_type": model}
        r = requests.post(CREATE_MODEL_URL, data=json.dumps(data), headers={'Authorization': 'Bearer ' + authToken})
        if "modelID" not in r.json():
            raise Exception(r.json())
        modelID = r.json()['modelID']
        print("model created with Id : {}".format(modelID))
        return modelID
    
    def __str__(self):
        return "modelID : {}".format(self.modelID)
    
    def uploadFile(self, filepath, dataFormat):
        if "UPLOAD_URL" not in URL_DICT[self.version]:
            raise Exception("Version {} does not support uploading".format(self.version))
        UPLOAD_URL = URL_DICT[self.version]["UPLOAD_URL"]
        path = Path(filepath)
        total_size = path.stat().st_size
        filename = path.name

        with tqdm(
                desc=filename,
                total=total_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
        ) as bar:
            with open(filepath, "rb") as f:
                fields = {"format": dataFormat, "modelID": self.modelID}
                fields["file"] = (filename, f)
                e = MultipartEncoder(fields=fields)
                m = MultipartEncoderMonitor(
                    e, lambda monitor: bar.update(monitor.bytes_read - bar.n)
                )
                headers = {"Content-Type": m.content_type, 'Authorization': 'Bearer ' + self.authToken}
                response = requests.post(UPLOAD_URL, data=m, headers=headers)
                response_json = response.json()
        if "detail" not in response_json or response_json["detail"] != "Upload Successful":
            raise Exception(response_json)
        print("File Uploaded")

    def train(self, epochs=10):
        if "TRAIN_URL" not in URL_DICT[self.version]:
            raise Exception("Version {} does not support training".format(self.version))
        TRAIN_URL = URL_DICT[self.version]["TRAIN_URL"]
        STATUS_URL = URL_DICT[self.version]["STATUS_URL"]
        data =  {"epochs": epochs, "modelID": self.modelID}
        r = requests.post(url=TRAIN_URL, data=json.dumps(data), headers={"Authorization": "Bearer " + self.authToken})
        with tqdm(total=epochs) as bar:
            while True:
                r = requests.get(STATUS_URL, params={"modelID": self.modelID},
                                 headers={"Content-type": "application/json",
                                          "Authorization": "Bearer " + self.authToken})
                if r.json() == "No Model Found":
                    continue
                if (r.json()['training'] == 'Done'):
                    break
                dataDict = r.json()
                bar.update(dataDict["epoch"])
                if "loss" in dataDict["results"]:
                    bar.set_postfix({'loss': dataDict["results"]["loss"]})
                if "status" not in dataDict or dataDict["status"] == "OK" or dataDict["status"] == "Ok":
                    bar.set_description("Status: {}".format(dataDict["training"]))
                else:
                    bar.set_description("Status: {}".format(dataDict["status"]))
                time.sleep(1)
        if r.json()["training"] != "Done":
            raise Exception(r.json())

    def infer(self, imagePath, **kwargs):
        INFER_URL = URL_DICT[self.version]["INFER_URL"]
        with open(imagePath, "rb") as image:
            buff = base64.b64encode(image.read()).decode('utf-8')
            data = {"images" : buff,
                    "modelID": self.modelID}
            for key,value in kwargs.items():
                data[key] = value
            r = requests.post(INFER_URL,
                              data=data,
                              headers={"Authorization": "Bearer " + self.authToken})
        return r.json()

    def inferAsync(self, imagePaths):
        INFER_ASYNC_URL = URL_DICT[self.version]["INFER_ASYNC_URL"]
        if isinstance(imagePaths, str):
            imagePaths = [imagePaths]
        imageBuffs = [open(imagePath, "rb") for imagePath in imagePaths]
        buffs = [base64.b64encode(buff.read()).decode('utf-8') for buff in imageBuffs]
        data = {"images" : buffs,
                "modelID": self.modelID}
        for key,value in kwargs.items():
            data[key] = value
        r = requests.post(INFER_ASYNC_URL,
                          data=data,
                          headers={"Authorization": "Bearer " + self.authToken})
        for i in range(len(imageBuffs)):
            imageBuffs[i].close()
        return r.json()

    def getResults(self):
        RESULTS_URL = URL_DICT[self.version]["RESULTS_URL"]
        r = requests.get(RESULTS_URL, params={"modelID": self.modelID},
                         headers={"Content-type": "application/json",
                                  "Authorization": "Bearer " + self.authToken})
        return r.json()
