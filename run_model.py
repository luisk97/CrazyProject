import os
import torch
import PIL.Image as pil
from torchvision import transforms
import numpy as np

import time
from picamera import PiCamera
from io import BytesIO

import depth_decoder
import resnet_encoder

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

print("Loading encoder")
encoder = resnet_encoder.ResnetEncoder(18, False)
print("Loading decoder")
depth_deco = depth_decoder.DepthDecoder(num_ch_enc=encoder.num_ch_enc, scales=range(4))

print("Loading model")
loaded_dict_enc = torch.load("model/encoder.pth", map_location='cpu')
filtered_dict_enc = {k: v for k, v in loaded_dict_enc.items() if k in encoder.state_dict()}
encoder.load_state_dict(filtered_dict_enc)

loaded_dict = torch.load("model/depth.pth", map_location='cpu')
depth_deco.load_state_dict(loaded_dict)
print("Model loaded")

depth_deco.eval()

#Estimation proccess flow (3 cycles)
for i in range(3):
  start = time.time()
  #image_path = "prueba.jpg"
  image_path = "foo.jpg"
    
  with PiCamera() as camera:
    camera.resolution = (1024, 768)
    camera.start_preview()
    # Camera warm-up time
    time.sleep(2)
    camera.capture('foo.jpg')
    
  input_image = pil.open(image_path).convert('RGB')
  original_width, original_height = input_image.size
  
  feed_height = loaded_dict_enc['height']
  feed_width = loaded_dict_enc['width']
  input_image_resized = input_image.resize((feed_width, feed_height), pil.LANCZOS)

  input_image_pytorch = transforms.ToTensor()(input_image_resized).unsqueeze(0)

  startP = time.time()
  with torch.no_grad():
    print("Encoder")
    features = encoder(input_image_pytorch)
    
  with torch.no_grad():
    print("Decoder")
    outputs = depth_deco(features)
    
  endP = time.time()
  totalP = endP - startP
  print("Depth estimation time:")
  print(totalP)
  
  disp = outputs[("disp", 0)]
  
  disp_resized = torch.nn.functional.interpolate(disp,(original_height, original_width), mode="bilinear", align_corners=False)
  disp_resized_list = disp_resized.squeeze().cpu()
  
  date = "D"+str(time.strftime("%x")).replace("/","")+"H"+str(time.strftime("%X")).replace(":","")
  with open("depth"+date+".txt", "w") as output:
    output.write(str(disp_resized_list.tolist()))
    
  end = time.time()
  total = end - start
  print("Total cycle time:")
  print(total)
  print("Image resulted:")
  print(disp_resized_list)