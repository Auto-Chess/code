# Auto Chess Code
This git repository will hold the code for the Auto Chess project.

We will use Python version 3.6.

This README document will provide you with all steps necessary to get up and coding.

# Writting code
If you haven't first read the Setup section below.

Since we will all be basically editing the same file (`main.py`) we have to use some sort of technique to make sure we do not 
step on each other's toes. You could imagine the kind of problems we would have if 3 of us tried to change the same line of the 
same file all at once. It wouldn't really work too well. 

Luckily Git (That seemingly useless and annoying tool) helps us solve exactly the problem I described above. Git's main feature 
is that it allows many people to work on the same piece of code (From 4-5 people to thousands in a company). 

## Git Overview
If you feel like you already understand Git, skip.

Git is a tool that lets you track changes made to a files. It can also be used to back up code in the Cloud 
("The Cloud" is just another name for someone elses computer). 

### File Tracking
You have to explicitly tell Git which files to track changes to. 
If you don't tell Git to track a file then it won't. This might seem obvious 
but you have to keep this in mind. 

#### Command Line
This can be done on the command line via `git add <filename>`.

#### Source Tree
In SouceTree simply click the Checkbox next to the file (I don't actually have SourceTree so hmu if I'm wrong).

### Commits
A "Commit" in Git is a snapshot of the changes made to files Tracked by Git at a specific time. A series of 
Git Commits can show the history of a file (The changes made, when, and who).

Along with a Commit you usually also include a "Commit Message". This message describes the changes 
you have made to the files Git is tracking since the last Commit you made. Try to keep this message 
short and descriptive (Ex., "Fixed issues with LEDs blinking too fast", "Programmed game loop to use LCD")

#### Command Line
After you have added some files for Git to Track you can Commit changes made to those files with: `git commit -m <Commit Message>`

#### Source Tree
Once you have added some files for Git to Track you can Commit changes by clicking the "Commit" button on the top of the screen.
You will then be brough to a page where you can type your commit message. 

### Pushing
Earlier I mentioned how Git could be used to backup code to "The Cloud". 
The way we will do that is by "Pushing" the Commits (Commits = Record of changes we made) 
to another server.

When you Push your Commits to a server it will see that it doesn't have those Commits 
and update its version to reflect the changes you made. That way if your computer dies it 
won't be a huge problem because the server will have a copy of your work.

#### Command Line
Type `git push origin <branch>`.

`<branch>` will usually be `master`. See Branches section for more information.

#### Source Tree
Click the Push button in the top bar.

### Pulling
Just like we can Push our Commits up to a server, we can also Pull other's Commits down 
from a server. When we Pull from a server in Git all our computer does is ask the server 
for Commits that it doesn't have. 

This way we can get other peoples work.

#### Command Line
Run: `git pull origin <branch>`

#### Source Tree
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

#### Command Line
Type `git checkout -b <branch name>` to create a branch.
Let Noah merge your created branch back in with master.

#### Source Tree
Click the Branch button in the top bar and enter your branch name.
Let Noah merge your created branch back in with master.

## Using Git to code
You will be assigned individual tasks. 

Before you do anything make sure you are on the "master" Git Branch and have the most recent code.
You can do this by switching branches (Different depending on what you use for Git) and then Pulling. 
This will ensure you have the newest code.

Next create a new Git Branch for the task you are working on. It should have a **short** (2 words max) name 
that describes what you will be changing/creating/fixing/ect.

Make all your Commits on this Branch. Once you are done with your feature make sure you have Pushed all 
you changes (Commits) up to our server and contact Noah on Slack.


# Setup
This section describes how to get your computer set up so you can start coding.

## Summary
You will have to install Python version 3.6. This is aviable on OSX, Windows, and Linux (Techinically what our Raspberry Pi is running).

Look at the section below which referes to your operating system:

## Steps For OSX
- 1. Open the Terminal application and type:
    - `xcode-select --install` and hit enter
        - This will install some useful tools for writting code to your system
        - This might take a bit of time
	    - You might be asked for your password
    - `/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"` (<< Copypaste that, too long to write)
		- This will install a tool which helps us install other development tools
    - Then `brew install python3`
		- This will install Python version 3.6
- 2. That should be it
- 2. Check everything worked correctly by typing `python --version` in the terminal
    - This should say something like `Python 3.6.0`
	- If it doesn't ask for help in Slack
	
## Steps for Windows
- 1. Go to [The Python 3.6 Download Page](https://www.python.org/downloads/release/python-360/)
	- Scroll to the "Files" section all the way at the bottom
    - Click the link that says "Windows x86-64 executable installer"
- 2. Run the file you download and follow the installer instructions
- 3. Congrats your done!

## Steps for Linux
- 1. It should be installed under the name `python3`.
    - At least on our Raspberry Pi
- 2. If its not, sorry dude your fault for using Linux. Figure it out.
