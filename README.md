files.doebi.at
==============

this is the sourcecode of files.doebi.at

a simple file management platform i needed to distribute files to the public

features
--------

 * simple clean interface
 * fast way to download files
 * organize files into folders
 * client script for easily adding temporary files
 * pastebin mode


puppy
-----

 **pup.py** is a python script for fast adding files to your files-server
 usage: `pup <filename>`

 * uploads files to a system-folder called 'temp'
 * assigns the file a random 8-char hash
 * returns the full url on commandline

 example:
> pup screenshot.png 
> Successfully uploaded screenshot.png to http://files.doebi.at/temp/WQN2qHUg.

pastebin mode
-------------

 for simple and fast text and sourcecode exchange you can use **pin**

 * uses vims :TOhtml to highlight source code in your favourite colors
 * uploads files using **pup**

 example:
> pin snippet.text 
> Successfully uploaded snippet.text.html to http://files.doebi.at/temp/8qDcZwsH.
