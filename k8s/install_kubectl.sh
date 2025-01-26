#!/bin/bash

#using Curl Command:
#Step 1: Finding the System's CPU architecture:

lscpu

#Step 2: Download the Kubectl Binary ( For x86-64 based systems ):

curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

#Step 3: Validating the Downloaded Binary File (For x86-64 based systems):

curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"

#validation of the kubectl binary using the downloaded checksum file:

echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check

#Step 4: Making Binary File Executable:

chmod +x kubectl

#Step 5: Installing Kubectl:

sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

#Step 6: Verifying Installation:

kubectl version --client


