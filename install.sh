#!/bin/bash

#install dependencies and add desktop Entry

if ! [ -z `which apt-get` ]; # Debian
    then sudo apt-get install vlc python python-tkinter 2> /dev/null
fi
if ! [ -z `which dnf` ]; # Fedora
    then sudo dnf install vlc python python-tkinter 2> /dev/null
fi
if ! [ -z `which pacman` ]; # Arch Linux
    then sudo pacman install vlc python python-tkinter 2> /dev/null
fi

current_dir=`pwd`

##TODO: desktop entry does not start

echo "[Desktop Entry]

Type=Application
Version=1.0
Name=subman
Comment=A subtitle manager tool
Path="$current_dir"
Exec=python3.6 "$current_dir"/subman.py
Icon="$current_dir"/media/iconWhite.png
Terminal=true
Categories=Media;" | sudo tee /usr/local/share/applications/subman.desktop > /dev/null

sudo chmod 0777 /usr/local/share/applications/subman.desktop