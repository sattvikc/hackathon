#!/bin/bash

export PATH="/home/sattvik/anaconda3/bin:$PATH"
source activate hackathon

export PYTHONPATH=/home/sattvik/code/hackathon

cd /home/sattvik/code/hackathon
python workflow/server/run.py
