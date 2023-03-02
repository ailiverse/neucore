# MIT License

# Copyright (c) 2022 Ailiverse

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from tqdm import tqdm
from yaspin import yaspin

import requests
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

import json
import base64
import time
import random
from pathlib import Path

from .env import URL_DICT, SIGN_IN_URL, SIGN_UP_URL

from .uploadUtils import upload_in_chunks, IterableToFileAdapter

# ######################### CUSTOM FUNCTIONS ###################

# ######################### SIGNUP AND SIGNIN FUNCTIONS ###################

def signUp(email, password, confirm_password, organization):
    """
    Method for registering a user on Ailiverse API.
    It will return an authentication token.
  
    :param email: (str)
    :param password: (str)
    :param confirm_password: (str)
    :param organization: (str)
    :return: (str) authentication token
    """
    print("Please Visit console.ailiverse.com to sign up!")
    return {"details": "Please Visit console.ailiverse.com to sign up!"}

def signIn(email, password):
    """
    Method for logging in (in case you lost your Authentication Token) on Ailiverse API.    :param email: (str)
    :param password: (str)
    :return: (str) previous authentication token
    """
    print("Please Visit console.ailiverse.com to retrieve api key")
    return {"details": "Please Visit console.ailiverse.com to retrieve api key"}

# ######################### CLASS ###################

class Model:
    def __init__(self, authToken, modelID=None, model=None):
        '''
            Method for registering a model using the API

            If modelId is not specified it will generate a new modelId based on the model.

            However is both modelID and model is not specified unable to determine what model to use.

            :param authToken: (str) required
            :param modelId: (str) optional
            :param model: (str) optional
            :param version: (str) optional
        '''
        self.authToken = authToken
        self.version = "1" # leave the version in for now

        # create a new model if modelID is not specified
        if modelID is None and model is None:
            raise Exception("Please specify either modelID or model")
        elif modelID is None:
            model = "_".join(model.split(" "))
            modelID = self.createModel(authToken, model)
        else:
            print("model loaded with Id : {}".format(modelID))
        self.modelID = modelID

    def createModel(self, authToken, model):
        """
        During creation of model, create a spinning wheel
        """
        CREATE_MODEL_URL = URL_DICT[self.version]["CREATE_MODEL_URL"]
        data =  { "model_type": model}
        headers = {'Authorization': 'Bearer ' + authToken}
        json_data = json.dumps(data)
        with yaspin(text="preparing...") as spinner:
            resp = requests.post(CREATE_MODEL_URL, data=json_data, headers=headers, stream=True)
            for line in resp.iter_lines(chunk_size=10, delimiter=b"\n"):
                if line:
                    info = json.loads(line.decode())
                    if "status" in info:
                        spinner.text = info["status"]

        if "modelID" not in info:
            raise Exception(info)
        modelID = info['modelID']
        print("model created with Id : {}".format(modelID))

        return modelID
    
    def __str__(self):
        return "modelID : {}".format(self.modelID)
    
    def uploadFile(self, filepath, dataFormat="default"):
        '''
        Method for uploading a compressed file

        :param filepath: (str) The path to the zip file
        :param dataFormat: (str) the format of the data
        :return: (bool) indicating that the file has be successfully uploaded else throw exception
        '''
        if "UPLOAD_URL" not in URL_DICT[self.version]:
            raise Exception("Version {} does not support uploading".format(self.version))
        UPLOAD_URL = URL_DICT[self.version]["UPLOAD_URL"]
        path = Path(filepath)
        total_size = path.stat().st_size
        filename = path.name

        headers = {'Authorization': 'Bearer ' + self.authToken}
        with open(filepath, "rb") as f:
            data = {"format": dataFormat, "modelID": self.modelID}

            fields = {"format": dataFormat, "modelID": self.modelID}
            fields["file"] = (filename, f)
            e = MultipartEncoder(fields=fields)
            total_size = path.stat().st_size

            with yaspin(text="preparing for upload") as spinner:
                def updateSpinnerValue(value):
                    spinner.text = "preparing {}/{}".format(int(value/1024), int(total_size/1024))
                m = MultipartEncoderMonitor(
                    e, lambda monitor: updateSpinnerValue(min(monitor.bytes_read, total_size))
                )
                headers = {"Content-Type": m.content_type, 'Authorization': 'Bearer ' + self.authToken}
                resp = requests.post(UPLOAD_URL,
                                     data=m,
                                     headers=headers,
                                     stream=True)
                # resp = requests.post(UPLOAD_URL,
                #                      data=data,
                #                      files={"file": f},
                #                      headers=headers,
                #                      stream=True)
                for line in resp.iter_lines(chunk_size=10, delimiter=b"\n"):
                    if line:
                        info = json.loads(line.decode())
                        if "status" in info:
                            spinner.text = info["status"]

        print(info)
        if info.get("detail", None) == "Upload successful":
            print("File Uploaded")
            return True
        else:
            raise Exception(info)
            return False

    def train(self, epochs=10):
        '''
        Method for starting training

        :param epochs: (int) The number of epochs to train the model
        :return: (dict) The results of the training
        '''
        if "TRAIN_URL" not in URL_DICT[self.version]:
            raise Exception("Version {} does not support training".format(self.version))
        TRAIN_URL = URL_DICT[self.version]["TRAIN_URL"]
        STATUS_URL = URL_DICT[self.version]["STATUS_URL"]
        data =  {"epochs": epochs, "modelID": self.modelID}
        with yaspin(text="preparing for training") as spinner:
            resp = requests.post(url=TRAIN_URL,
                                 data=json.dumps(data),
                                 headers={"Authorization": "Bearer " + self.authToken},
                                 stream=True)
            for line in resp.iter_lines(chunk_size=10, delimiter=b"\n"):
                if line:
                    pass
        with tqdm(total=epochs) as bar:
            while True:
                r = requests.get(STATUS_URL, params={"modelID": self.modelID},
                                 headers={"Content-type": "application/json",
                                          "Authorization": "Bearer " + self.authToken})

                try:
                    dataDict = r.json()
                    if dataDict == "No Model Found":
                        continue
                    if (dataDict['training'] == 'Done') or (dataDict.get("status", None) == "Error"):
                        break
                    bar.update(dataDict["epoch"])
                    if "loss" in dataDict["results"]:
                        bar.set_postfix({'loss': dataDict["results"]["loss"]})
                    if "status" not in dataDict or dataDict["status"] == "OK" or dataDict["status"] == "Ok":
                        bar.set_description("Status: {}".format(dataDict["training"]))
                    else:
                        bar.set_description("Status: {}".format(dataDict["status"]))
                except Exception as e:
                    continue

            try:
                if r.json()["training"] != "Done":
                    raise Exception(r.json())
            except Exception as e:
                print("Failed to train")
                raise Exception(r)


    def infer(self, imagePath, **kwargs):
        '''
        Performing an Inference on a single image

        :param imagePath: (str) The location to the image
        :param kwargs: (dict) Any additional arguments to be pass to the api
        :return: (dict) The inference result 
        '''
        INFER_URL = URL_DICT[self.version]["INFER_URL"]
        with open(imagePath, "rb") as image:
            buff = base64.b64encode(image.read()).decode('utf-8')
            data = {"images" : buff,
                    "modelID": self.modelID}
            for key,value in kwargs.items():
                data[key] = value
            headers = {"Authorization": "Bearer " + self.authToken}
            with yaspin(text="preparing...") as spinner:
                resp = requests.post(INFER_URL, data=data, headers=headers, stream=True)
                for line in resp.iter_lines(chunk_size=10):
                    if line:
                        info = json.loads(line.decode())
                        if "status" in info:
                            spinner.text = info["status"]
        return info

    def inferAsync(self, imagePaths, **kwargs):
        '''
        Performing an Inference on a single image (Async)

        :param imagePaths: (list of str) locations to multiple images
        :param kwargs: (dict) Any additional arguments to be pass to the api
        :return: (dict) to indicate if the model has successfully started inference
        '''
        INFER_ASYNC_URL = URL_DICT[self.version]["INFER_ASYNC_URL"]
        if isinstance(imagePaths, str):
            imagePaths = [imagePaths]
        imageBuffs = [open(imagePath, "rb") for imagePath in imagePaths]
        buffs = [base64.b64encode(buff.read()).decode('utf-8') for buff in imageBuffs]
        data = {"images" : buffs,
                "modelID": self.modelID}
        for key,value in kwargs.items():
            data[key] = value
        headers = {"Authorization": "Bearer " + self.authToken}
        json_data = json.dumps(data)
        with yaspin(text="preparing...") as spinner:
            resp = requests.post(INFER_ASYNC_URL, data=json_data, headers=headers, stream=True)
            for line in resp.iter_lines(chunk_size=10):
                if line:
                    info = json.loads(line.decode())
                    if "status" in info:
                        spinner.text = info["status"]

        for i in range(len(imageBuffs)):
            imageBuffs[i].close()

        print("Inference Started")
        return True


    def getResults(self):
        '''
        Get results from the inference

        :return: (dict) The inference result 
        '''
        RESULTS_URL = URL_DICT[self.version]["RESULTS_URL"]
        r = requests.get(RESULTS_URL, params={"modelID": self.modelID},
                         headers={"Content-type": "application/json",
                                  "Authorization": "Bearer " + self.authToken})
        return r.json()
