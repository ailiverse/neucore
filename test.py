"""
This is an example for version 1 models
"""
import neucore

email = "YOUR_EMAIL_HERE"
password = "YOUR_PASSWORD_HERE"
confirm_password = "YOUR_PASSWORD_HERE"
organization = "YOUR_ORGANIZATION_HERE"

# sign up 
authToken = neucore.signUp(email, password, confirm_password, organization)

# Uncomment if your email is already registered, however, you've lost your token
# authToken = neucore.signIn(email, password)

model = neucore.Model(authToken, model="Image Segmentation")

model.uploadFile("train.zip", "labelme")

model.train(epochs=10)

results = model.infer("hen.jpg")

print(results)
