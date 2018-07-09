# subman
A python script for launching video and subs (not necessarily) from specified folder and keeping record of watched videos.  
  
<h3>Preview</h3> 
  
![Alt text](media/Screenshots/screen01?raw=true "Screenshot")


<h3>Requirements</h3>  
vlc, python3.6, tkinter (automatically installed by install.sh)  
  
  
<h3>Installation</h3>   
On linux, launch install.sh (will install dependencies and add the desktop entry).  

<h3>Usage</h3>  
Videos must have the same format name and extension (also subtitles) and 2 digit for the episode;
<b>Recognized video extensions</b>: .mkv .avi .mp4 .mpeg .flv .wmv
<b>Recognized subtitles extension</b>: .srt .vtt .scc

For example:  
```
VideosFolder/
  Episode01
  Episode02
SubsCasualName/
  Sub01  
  Sub02  
```
```
RandomName/
  01EpisodeDVD
  02EpisodeDVD
  Sub01WhateverYouWantIJustCareAboutExtension
  Sub02WhateverYouWantIJustCareAboutExtension
```
Will work.  

  
	  
Viceversa:  
```
Videos/  
  Episode01  
  Episode03
  Sub01  
  Sub02  
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
Will not work.  
