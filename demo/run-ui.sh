#!/bin/bash

export PATH="/home/sattvik/anaconda3/bin:$PATH"
source activate hackathon

export PYTHONPATH=/home/sattvik/code/hackathon

cd /home/sattvik/code/hackathon/workflowui
python manage.py runserver 0.0.0.0:2887
