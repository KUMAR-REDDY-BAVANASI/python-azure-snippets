# Azure_Python



Getting Started with Azure SDK in Python
=========================================


Step1:  If you don't already have it, install Python.
======
        This Azure SDK is compatible with Python 2.7, 3.4, 3.5, 3.6 and 3.7.
        
sudo apt update -y && apt upgrade -y

sudo apt install python3-pip

Step2:  Install and initialize the virtual environment with the "venv" module on Python3.
======

apt-get install python3-venv

python3 -m venv .venv

cd .venv

source bin/activate

Step3:  Clone the repository
======

git clone https://github.com/KUMAR-BAVANASI/Azure_Python.git


Step4:  Install the dependencies using pip.
======

cd Azure_Python/

sudo pip3 install -r requirements-azure-python.txt


Step5: For any Error came related to this, you will install these two dependencies.
======

pip3 install setuptools_rust

pip3 install --upgrade pip

sudo pip3 install -r requirements-azure-python.txt

Step6:  Fill in and export these environment variables into your current shell.
======

export AZURE_TENANT_ID={your tenant id}

export AZURE_CLIENT_ID={your client id}

export AZURE_CLIENT_SECRET={your client secret}

export AZURE_SUBSCRIPTION_ID={your subscription id}

Like,

export AZURE_TENANT_ID=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

export AZURE_CLIENT_ID=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

export AZURE_CLIENT_SECRET=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

export SUBSCRIPTION_ID=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX



Step7:  Run the python script.
======

python3 filename.py
