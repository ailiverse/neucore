url="https://api.ailiverse.com"

SIGN_UP_URL="{}/signUp".format(url)
SIGN_IN_URL="{}/signIn".format(url)
CREATE_MODEL_URL="{}/createModel".format(url)
UPLOAD_URL="{}/userUpload".format(url)
STATUS_URL="{}/status".format(url)
TRAIN_URL="{}/train".format(url)
INFER_URL="{}/infer".format(url)
INFER_ASYNC_URL="{}/inferAsync".format(url)
RESULTS_URL="{}/results".format(url)

url_2 = "http://34.80.13.82:8085"

SIGN_UP_URL_2="{}/signUp".format(url_2)
SIGN_IN_URL_2="{}/signIn".format(url_2)
CREATE_MODEL_URL_2="{}/createModel".format(url_2)
INFER_URL_2="{}/infer".format(url_2)
INFER_ASYNC_URL_2="{}/inferAsync".format(url_2)
RESULTS_URL_2="{}/results".format(url_2)

URL_DICT = {
    "1" : { "SIGN_UP_URL" : SIGN_UP_URL, # version 1
            "SIGN_IN_URL" : SIGN_IN_URL,
            "CREATE_MODEL_URL": CREATE_MODEL_URL,
            "UPLOAD_URL": UPLOAD_URL,
            "STATUS_URL": STATUS_URL,
            "TRAIN_URL": TRAIN_URL,
            "INFER_URL": INFER_URL,
            "INFER_ASYNC_URL": INFER_ASYNC_URL,
            "RESULTS_URL": RESULTS_URL},
    "2" : {
        "SIGN_UP_URL": SIGN_UP_URL_2, # version 2
        "SIGN_IN_URL": SIGN_IN_URL_2,
        "CREATE_MODEL_URL": CREATE_MODEL_URL_2,
        "INFER_URL": INFER_URL_2,
        "INFER_ASYNC_URL": INFER_ASYNC_URL_2,
        "RESULTS_URL": RESULTS_URL_2
    }
}
