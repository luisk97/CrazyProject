from six.moves import urllib
import zipfile

model_url = "https://storage.googleapis.com/niantic-lon-static/research/monodepth2/mono_640x192.zip"
model_path = "model"

print("Downloading model...")
urllib.request.urlretrieve(model_url, model_path + ".zip")
print("Model downloaded")

with zipfile.ZipFile(model_path + ".zip", 'r') as f:
  f.extractall(model_path)
print("Model unziped")
