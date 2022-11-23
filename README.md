# CrazyProject
### Execution of a monocular depth estimation model on an embedded system (Raspberry Pi Zero)

Model taked from: https://github.com/nianticlabs/monodepth2

Colab testing environment: https://colab.research.google.com/drive/1TXeI7PwdrbFNWTkw7RTdptvMD4-pAV2V?usp=sharing

![image](https://user-images.githubusercontent.com/30986170/203466630-5878aa59-62fa-4748-bda2-5b5f39ad86d3.png)

***
## Proccess to set up the project in Raspberry Pi Zero

Model: Raspberry Pi Zero W V1.1

Architecture: armv6 32bits
***

### Steps:
- First Install Raspbian
  - Reset a MicroSD and install Raspian OS on it
- Update Linux package handler
  -		sudo apt-get update
  -		sudo apt-get upgrade
- Enable camera
  -		sudo raspi-config
  - Select Interfaces Option
  
  ![image](https://user-images.githubusercontent.com/30986170/203469472-1d89bc09-aa75-40e0-8427-daef77542e1c.png)
  - Legacy camera
  
  ![image](https://user-images.githubusercontent.com/30986170/203469517-ee12d351-b42f-4d69-b887-fdaaea24733f.png)
  - Enable
- Install python 3.7
  - Follow steps in: https://programmerclick.com/article/3973980601/
- Update pip
  -		python -m pip install --user --upgrade pip
  - Check version:
  -		python -m pip --version
- Install torch
  -	Git Raspberry Pi Zero V1 compatible torch versions: https://github.com/nmilosev/pytorch-arm-builds
  - Steps:
    - Install necessary libraries: 
    -		sudo apt install libopenblas-dev libblas-dev m4 cmake python3-dev python3-yaml python3-setuptools python3-wheel python3-pillow python3-numpy
    - Download versions in the git:
    -		wget https://github.com/nmilosev/pytorch-arm-builds/archive/refs/heads/master.zip
    -		unzip master.zip
    -		cd pytorch-arm-builds-master/
    - Install armv6 compatible torch and torchvision versions:
    -		python -m pip install --user ./torch-1.1.0-cp37-cp37m-linux_armv6l.whl ./torchvision-0.3.0-cp37-cp37m-linux_armv6l.whl
    -	Fix Pillow error:
		-		python -m pip uninstall pillow
		-		python -m pip install --user "pillow<7"
    - Veryfy by running:
    -		python inference.py <image path>
- Install PiCamera
  -		python -m pip install --user picamera
- Download the project scripts from this git on your Raspberry Pi and run it
***
