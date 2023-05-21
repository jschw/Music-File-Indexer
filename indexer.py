import os
import sys
from pathlib import Path
import re
import shutil
from datetime import date
from mutagen.easyid3 import EasyID3
from mutagen.easymp4 import EasyMP4
from mutagen.wave import WAVE


def getsongobject(file):
    mp4_extensions = ["m4a", "m4p", "m4v"]
    if any(file.endswith(ext) for ext in mp4_extensions):
            songobject = EasyMP4(file)
    elif file.endswith(".wav"):
            songobject = WAVE(file)
    else: #assumes other files are mp3
            songobject = EasyID3(file)
    return songobject


albumlist = {}

if sys.platform.startswith('darwin'):
    application_path = Path(os.path.dirname(os.path.abspath(__file__))).parent
else:
    application_path = os.path.abspath(".")

for root, dirs, files in os.walk(application_path):
    for file in files:
        if file.endswith(".mp3") or file.endswith(".m4a") or file.endswith(".m4v"):

            try:
                song = getsongobject(os.path.join(root, file))
                artist = 'Unknown Artist'

                if 'artist' in song.keys():
                        artist = song['artist'][0]

                album = 'Unknown Album'
                if 'album' in song.keys():
                        album = song['album'][0]
                
                if album not in albumlist:
                    albumlist[album] = artist
                
                # artistalbum = f"{artist[0]} - {album[0]}"
                # print(artistalbum)

            except Exception as e:
                    print(f"Error reading meta info in file {os.path.join(root, file)}")
                    # print(str(e))


# Print in text file
out_path = os.path.join(application_path, "albumlist.txt")
print(f"Write TXT file to: {out_path}")

with open(out_path, 'w') as output_file:
    now = date.today()

    output_file.write("========= Album Catalog ===========\n")
    output_file.write("===================================\n")
    output_file.write(f"==== Last update: {now.day}.{now.month}.{now.year} =====\n")
    output_file.write("\n")

    number = 1
    for album, artist in albumlist.items():
        output_file.write(f"{number}:\t{artist} - {album}\n")
        number += 1

# Print in csv file
out_path = os.path.join(application_path, "albumlist.csv")
print(f"Write CSV file to: {out_path}")

with open(out_path, 'w') as output_file:
    output_file.write("Artist;Album\n")
    for album, artist in albumlist.items():
        output_file.write(f"{artist};{album}\n")
