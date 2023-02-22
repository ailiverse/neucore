
# Table of Contents

1.  [Installation](#orgc64ab88)
2.  [Usage](#org32451d6)

This is the pypi package for Ailiverse AI models


<a id="orgc64ab88"></a>

# Installation
    git clone https://github.com/ailiverse/neucore
    
    cd neucore
    
    pip install .

<a id="org32451d6"></a>

# Usage
The following are the models implemented
-   Image Segmentation
-   Image Classification
-   Deep Fake Detection
-   Text Guided Segmentation

**Note Text Guided Segmentation does not have training or upload functions**

    import neucore
    
    authToken = "Your_AuthToken_Here" # visit console.ailiverse.com to obtained your auth token if you have not already

    # defined the model
    model = neucore.Model(authToken, model="Image Segmentation")
    # If you still want to use the same model Id uncomment the following code
    # model = neucore.Model(authToken, modelID = "YOUR_MODELID_HERE", model="Image Segmentation")
    
    model.uploadFile("train.zip", "labelme")
    
    model.train(epochs=1) # By default the number of epochs is 10
    
    results = model.infer("hen.jpg")
    
    print(results)
    
**Note you can use the modelID argument when initalizing the neucore model to if you want to use the previous models**
