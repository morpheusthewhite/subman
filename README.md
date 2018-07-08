# subman
A python script for launching video and subs (not necessarily) from specified folder and keeping record of watched videos.  
  
<h3>Preview</h3> 
  
![Alt text](media/Screenshots/screen01?raw=true "Screenshot")


<h3>Requirements</h3>  
vlc, python3.6, tkinter (automatically installed by install.sh)  
  
  
<h3>Installation</h3>   
On linux, launch install.sh (will install dependencies and add the desktop entry).  

<h3>Usage</h3>  
Videos and subtitles must be in separated folder and each one should contains only videos or subtitles with the same format name (and 2 digit for the episode);    
  
For example:  
```
Videos/  
  Episode01  
  Episode02  
Subtitles/  
  Sub01  
  Sub02  
```
Will work.  

  
	  
Viceversa:  
```
Videos/  
  Episode01  
  Episode03  
Subtitles/  
  Sub01  
  Sub02  
  ```
```
Videos/  
  Episode01  
  Episode02  
Subtitles/  
  Sub01  
  Sub02  
  Folder1/  
 ``` 
```
Videos/  
  Episode00  
  Episode02  
Subtitles/  
  Sub01  
  Sub02  
```
```
Videos/  
  Episode1  
  Episode2  
Subtitles/  
  Sub1  
  Sub2  
```    
```
Season1/  
  Episode01  
  Episode02  
  Sub01  
  Sub02  
 ``` 
Will not work.  
