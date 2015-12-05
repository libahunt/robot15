#!/bin/bash
# Update code from github and start main.py of robot15-project

echo "Hello, world! In main.sh";

cd ~/robot15-project/
echo "Pulling Python code from git ...";
git checkout Maze.pyc #this file prevents git from pulling
git pull origin master;

cd ~/sketchbook/robot15_arduino/
echo "Pulling Arduino code from git ...";
git pull origin master;

cd ~/robot15-project/
python main.py;
