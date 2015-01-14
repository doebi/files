files.doebi.at
==============

this is the sourcecode for files.doebi.at
a simple file management platform i needed to distribute files to the public

## features

 * simple clean interface
 * fast way to share files
 * organize files into folders
 * md-files are rendered to proper HTML
 * client script for easily adding temporary files
 * pastebin mode

## workflow

![workflow](http://files.doebi.at/temp/ALJ9DaWg)

1. [Sender] Upload a file using either a web based client the commandline client
2. [Server] Store File on Fileserver and report back the unique url
3. [Sender] Share the url
4. [Receiver] Dowload file


## puppy (commandline client)

 **pup.py** is a python script for fast adding files to your files-server
 usage: `pup <filename>`

 * uploads files to a system-folder called 'temp'
 * assigns the file a random 8-char hash
 * returns the full url on commandline

 example:
 
> pup screenshot.png

> Successfully uploaded screenshot.png to http://files.doebi.at/temp/WQN2qHUg.

## pastebin mode

 for simple and fast text and sourcecode exchange you can use **pin**

 * uses vims :TOhtml to highlight source code in your favourite colors
 * uploads files using **pup**

 example:
 
> pin snippet.text

> Successfully uploaded snippet.text.html to http://files.doebi.at/temp/8qDcZwsH.

## planned features

 * automatically delete temporary files after a certain time
 * security (E2E)

## security

Unfortunately, as of now there is no security at all.
But with the current architecture it can easily be added anytime, asuming key exchange has already happened elsewhere.
