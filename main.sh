#!/bin/bash
# testing...

echo "Hello, world! In main.sh";

cd ~/robot15-project/

echo "Pulling from git ...";

git pull origin master;

python main.py;
