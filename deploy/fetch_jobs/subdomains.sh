#!/bin/bash

set -x



cd deploy/fetch_jobs
sudo apt install python3-venv -y
python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python3 subdomains.py