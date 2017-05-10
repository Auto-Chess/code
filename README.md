# Auto Chess Code [![Build Status](https://travis-ci.org/Auto-Chess/code.svg?branch=master)](https://travis-ci.org/Auto-Chess/code)
This git repository will hold the code for the Auto Chess project.

We will use Python version 3.6.

This README document will provide you with all steps necessary to get up and coding.

# Witting code
If you haven't, first read the [Setup](#markdown-header-setup) section below.

Since we will all be basically editing the same file (`main.py`) we have to use some sort of technique to make sure we 
do not step on each other's toes. You could imagine the kind of problems we would have if 3 of us tried to change the 
same line of the same file all at once. It wouldn't really work too well. 

Luckily Git (That seemingly useless and annoying tool) helps us solve exactly the problem I described above. Git's main 
feature is that it allows many people to work on the same piece of code (From 4-5 people to thousands in a company). 

## Git Overview
If you feel like you already understand Git, skip this entire section.
This section will provide a general overview of what Git is and how we will use to help code our project.    

Git is a tool that lets you track changes made to a files. It can also be used to back up code in the Cloud 
("The Cloud" is just another name for someone else's computer). 

### File Tracking
You have to explicitly tell Git which files to track changes to. 
If you don't tell Git to track a file then it won't. This might seem obvious 
but you have to keep this in mind. 

###### Command Line instructions
You can tell Git to Track a file by typing:
```bash
git add <filename>
```
in your command line and hitting enter. 

Replace `<filename>` with the file you want Git to track

###### Source Tree instructions
In SouceTree simply click the Checkbox next to the file (I don't actually have SourceTree so hmu if I'm wrong).

### Commits
A "Commit" in Git is a snapshot of the changes made to files Tracked by Git at a specific time. A series of 
Git Commits can show the history of a file.

A Git Commit consists of 2 parts:
- The first part is changes to any files Tracked by Git
- The second part is a short message that describes the changes in the first part
    - This should be **short**, like max **2 words**
    - Try to be descriptive (ex., "Fixed LED blinking issue" or "Programmed game loop to use LCD")

###### Command Line instructions
After you make some changes to files Git is tracking you can Commit those changes. You do this by typing:
```bash
git commit -m "<Commit Message>"
```
in your command line and hitting enter.

The `-m` tells the Git tool that the following text is your *Commit Message*.  
Replace `<Commit Message>` with your short and clear commit message (Don't forget to surround with quotes)

###### Source Tree instructions
After you make some changes to files Git is tracking you can Commit those changes. In SourceTree you do this by clicking 
the "Commit" button in the upper bar. You will then be able to type your Commit Message into a box located in the lower 
left-ish part of your screen.

### Pushing
Earlier I mentioned how Git could be used to backup code to "The Cloud". 
The way we will do that is by "Pushing" the Commits (Commits = Record of changes we made) to another server.

When you Push your Commits to a server it will see that it doesn't have those Commits 
and update its version to reflect the changes you made. That way if your computer dies it 
won't be a huge problem because the server will have a copy of your work.

**ALWAYS Commit *then* Pull** (Don't worry Pulling will be explained in the next section) before pushing.

###### Command Line instructions
Type:
```bash
git push origin <branch>
```
into your terminal and hit enter.

`origin` is the name of the server you are Pushing your commit's to.
`<branch>` is the name of the Branch you are pushing (Don't worry Branches will be explained after the next section)

###### Source Tree instructions
Click the Push button in the top bar.

### Pulling
Just like we can Push our Commits up to a server, we can also Pull other people's Commits  
from a server. When we Pull from a server in Git all our computer does is ask the server 
for Commits that we do not have. 

This way we can get other peoples work.

**ALWAYS Commit *then* Pull** before pushing. Do this just in case anybody has done any work since the last 
time you Pulled (The chances that someone has are quite high).

###### Command Line instructions
Type:
```bash
git pull origin <branch>
```
into your terminal and hit enter.

Where `<branch>` is the branch you want to Pull for.

###### Source Tree instructions
Click the Pull button in the top bar.

### Branches
Every time you make a Commit in Git you make that Commit on a certain "Branch". 
Branches are just ways to seperate the work you are doing from someone elses. The 
Commits you make on one Branch will not effect the files on another Branch.

The default branch is called "master". This is where the "main" copy of the code will be. 
Every time you go to make a change to this code first make a Branch from "master".

This way while you are making your changes other people won't have to deal with you 
changing files until you have finished. Once you have completed your changes you 
"Merge" (Aka Combine) your Branch back in with the "master" branch.

###### Command Line instructions
Type `git checkout -b <branch name>` to create a branch.
Let Noah merge your created branch back in with master.

###### Source Tree instructions
Click the Branch button in the top bar and enter your branch name.
Let Noah merge your created branch back in with master.

## Using Git to code
You will be assigned individual tasks on BitBucket.org. 

Before you do anything make sure you are on the "master" Git Branch and have the most recent code.
You can do this by switching branches (Different depending on what you use for Git) and then Pulling. 
This will ensure you have the newest code.

Next create a new Git Branch for the task you are working on. It should have a **short** (2 words max) name 
that describes what you will be changing/creating/fixing/ect.

Make all your Commits on this Branch. Once you are done with your feature make sure you have Pushed all 
you changes (Commits) up to our server and contact Noah on Slack.

## Running our code
If you have completed the setup step then simply open a terminal up in the directory of the `main.py` file 
and run `python ./main.py`.


# Setup
This section describes how to get your computer set up so you can start coding.

## Summary
You will have to install Python version 3.6. This is available on OSX, Windows, and Linux (Techinically what our Raspberry Pi is running).

Look at the section below which referes to your operating system:

## Steps For OSX
- Open the Terminal application and type:
    - `xcode-select --install` and hit enter
        - This will install some useful tools for writting code to your system
        - This might take a bit of time
	    - You might be asked for your password
    - `/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"` (<< Copypaste that, too long to write)
		- This will install a tool which helps us install other development tools
    - Then `brew install python3`
		- This will install Python version 3.6
- That should be it
- Check everything worked correctly by typing `python --version` in the terminal
    - This should say something like `Python 3.6.0`
	- If it doesn't ask for help in Slack
- Now that you are done go back up to the [Writting Code section](#markdown-header-writting-code)
	
## Steps for Windows

- Go to [The Python 3.6 Download Page](https://www.python.org/downloads/release/python-360/)
    - Scroll to the "Files" section all the way at the bottom
    - Click the link that says "Windows x86-64 executable installer"
- Run the file you download and follow the installer instructions
- Congrats your done!
- Now that you are done go back up to the [Writting Code section](#markdown-header-writting-code)

## Steps for Linux
The steps depend on the distribution of Linux you are running.

- If you are using Ubuntu Python 3.6 should already be installed under the name `python3`
    - If it is not installed install it with the `apt-get install python3` command (You may need to run this with `sudo`)
    - Our Raspberry Pi runs a version of Ubuntu called "Raspbian"
- If you are using Arch Linux you can install Python 3.6 under the official package `python`
    - If it is not installed install it with `pacman -S python` (You may need to run this with `sudo`)
- If you Linux distribution is not listed above:
    - Search around and see if your distribution has an official package to install
    - Otherwise go to the [Python 3.6 webpage](https://www.python.org/downloads/release/python-360/) and download the best file and install
- Now that you are done go back up to the [Writting Code section](#markdown-header-writting-code)

# Connecting
- `sudo bash -c "echo 1 > /proc/sys/net/ipv4/ip_forward"`
- `sudo iptables -t nat -A POSTROUTING -o wlp58s0 -j MASQUERADE`
- `sudo ifconfig enp57s0u1 10.0.0.1 netmask 255.255.255.0 up`
- to `/etc/dhcpd.conf` > 
```
subnet 10.0.0.0 netmask 255.255.255.0 {
    range 10.0.0.100 10.0.0.120;
    option routers 10.0.0.1;
    option domain-name-servers the-ip-address-you-have-in-etc-resolv.conf;
}
```
- `sudo systemctl start dhcpd4.service`
