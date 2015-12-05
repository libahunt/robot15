#!/bin/bash
# Update code from github and start main.py of robot15-project

echo "Hello, world! In main.sh";


cd ~/sketchbook/robot15_arduino/
echo "Pulling Arduino code from git ...";
git pull origin master;

cd ~/robot15-project/
echo "Pulling Python code from git ...";
git pull origin master;

python main.py;
