
# Table of Contents

1.  [Installation](#orgd92d58e)
2.  [Usage](#orgadc4d4e)
    1.  [Version 1](#orge8e2ab9)
    2.  [Version 2](#org5cfe22f)

This is the pypi package for Ailiverse AI models


<a id="orgd92d58e"></a>

# Installation

    git clone https://github.com/ailiverse/neucore
    
    cd neucore
    
    pip install .


<a id="orgadc4d4e"></a>

# Usage


<a id="orge8e2ab9"></a>

## Version 1

This is a simple use case for version 1 models which include

-   Image Segmentation
-   Image Classification
-   Deep Fake Detection

    import neucore
    
    email = YOUR_EMAIL_HERE
    password = YOUR_PASSWORD_HERE
    confirm_password = YOUR_PASSWORD_HERE
    organization = YOUR ORGANIZATION HERE
    
    # sign up 
    authToken = neucore.signUp(email, password, confirm_password, organization)
    
    # Uncomment if your email is already registered, however, you've lost your token
    # authToken = neucore.signIn(email, password)
    
    # defined the model
    model = neucore.Model(authToken, model="Image_Segmentation", version="1")
    # If you still want to use the same model Id uncomment the following code
    # model = neucore.Model(authToken, modelID = "YOUR_MODELID_HERE", model="Image_Segmentation", version="1")
    
    model.uploadFile("train.zip", "labelme")
    
    model.train(epochs=1) # By default the number of epochs is 10
    
    results = model.infer("hen.jpg")
    
    print(results)

**Note you can use the modelID argument when initalizing the neucore model to if you want to use the previous models**


<a id="org5cfe22f"></a>

## Version 2

This is a simple example for version 2 models which include

-   Text Guided Image Segmentation

**Note version 2 models does not have training or upload functions**
The following example is for text guided image segmentation

    import neucore
    
    email = YOUR_EMAIL_HERE
    password = YOUR_PASSWORD_HERE
    confirm_password = YOUR_PASSWORD_HERE
    organization = YOUR ORGANIZATION HERE
    
    # sign up 
    authToken = neucore.signUp(email, password, confirm_password, organization)
    
    # Uncomment if your email is already registered, however, you've lost your token
    # authToken = neucore.signIn(email, password)
    
    # defined the model
    model = neucore.Model(authToken, model="Text_Guided_Segmentation", version="1")
    # If you still want to use the same model Id uncomment the following code
    # model = neucore.Model(authToken, modelID = "YOUR_MODELID_HERE", model="Image_Segmentation", version="1")
    
    results = model.infer("hen.jpg", texts=["hen"])
    
    print(results)

