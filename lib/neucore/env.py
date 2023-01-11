url="http://35.197.135.77:8085"

SIGN_UP_URL="{}/signUp".format(url)
SIGN_IN_URL="{}/signIn".format(url)
CREATE_MODEL_URL="{}/createModel_load".format(url)
UPLOAD_URL="{}/userUpload".format(url)
STATUS_URL="{}/status".format(url)
TRAIN_URL="{}/train".format(url)
INFER_URL="{}/infer_load".format(url)
INFER_ASYNC_URL="{}/inferAsync_load".format(url)
RESULTS_URL="{}/results".format(url)

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
}
