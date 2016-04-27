#!/bin/bash

<<<<<<< HEAD:deps_install.sh
sudo apt-get install libxml2-dev libxslt-dev python-dev python3-lxml -y
=======
clear
echo "Installing the dependencies on OS-side"
sudo apt-get install g++ -y 
>>>>>>> my-2nd-branch:deps_install
sudo apt-get install g++ -y
sudo apt-get install pandoc -y
pip install -r requirements.txt


