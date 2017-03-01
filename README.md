# Auto Chess Code
This git repository will hold the code for the Auto Chess project.

We will use Python version 3.6.

This README document will provide you with all steps necessary to get up and coding.

# How do I do stuff?
First read the "How do I get set up?" section to setup your computer.

Then look at the Issue Tracker for any issues that you are assigned to and do those.

# How do I get set up?
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
