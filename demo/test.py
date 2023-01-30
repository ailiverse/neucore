import neucore

authToken = "Your_AuthToken_Here" # visit console.ailiverse.com to obtained your auth token if you have not already

model = neucore.Model(authToken, model="Image Segmentation")

model.uploadFile("train.zip", "labelme")

model.train(epochs=10)

results = model.infer("hen.jpg")

print(results)
