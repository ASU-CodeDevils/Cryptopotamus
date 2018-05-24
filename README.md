# Cryptopotamus
E2EE messaging
May 23, 2018:

Started the basic shell for playing with E2EE messaging.
This is based on Django which is heavily supported, making it extemely likely you will find
answers to your questions.
At this stage, it would be interesting to set the landing page to one room.
In this single room, you can enter a username and an encryption key. Once this is entered,
messages which match your encryption key will be decrypted in the chat window. Others will remain encrypted.
Messages you send will be encrypted using the key you provided.
This is the plan at this stage.

Instruction for launching the server are given for an Ubuntu installation.
Fairly easy to install ubuntu in a virtualbox.

This is a Django App based on the multichat application found here:
https://github.com/andrewgodwin/channels-examples

Installation
You will need Python 3.6
You will need Pip3
You will need paver
You will need python-dev
You will need Redis

If you're using Ubuntu:

Install python3.6
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.6

Install Pip3
sudo apt-get install python3-pip

Install paver
sudo apt-get install python-paver

Install python-dev
sudo apt-get install python3.6-dev

(The original creator used a docker container. We may do this again, but the walk-through is very complete.)
Install Redis
https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-redis-on-ubuntu-16-04

You can use the paver script for the rest of the process.
Install Virtual Environment:
paver Install

Start bash terminal in virtual environment:
paver bash

To exit bash terminal:
exit

Start the server:
paver run
