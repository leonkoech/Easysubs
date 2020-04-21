import os
import hashlib
import requests
import argparse
from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog

"""simple script to obtain subtitle from subdb.com
usage: python2 subtitler.py <moviefilename>"""


def get_hash(name):
    readsize = 64 * 1024
    with open(name, 'rb') as f:
        size = os.path.getsize(name)
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()


def request_sub(md5):
    md5 = md5
    url = "http://api.thesubdb.com/?action=download&hash="+md5+"&language=en"
    header = {'user-agent': 'SubDB/1.0 (subtitler/0.1)'}
    r = requests.get(url, headers=header)
    if r.status_code == 200:
        return r.content
    else:
        return "something nasty happened"


def save_sub(data, filename):
    s_filename = filename[:-4] + ".srt"
    with open(s_filename, "w+") as s_f:
        s_f.write(data)


def subs(filename):
    md5 = get_hash(filename)
    data = request_sub(md5)
    save_sub(data, filename)



def selectfile():
    #this method presents the user with  gui to select the movie file
    root=Tk()
    root.withdraw() 
    root.filename =tkFileDialog.askopenfilename(initialdir = "C:/Users/LEON KIPKOECH/Downloads/Bad Boys For Life (2020) [720p] [WEBRip] [YTS.MX]/",title = "Select movie file",filetypes = (
    ("all files","*.*"),
    ("ASF files", "*.ASF"),
    ("FLAC files", "*.FLAC"),
    ("FLV files", "*.FLV"),
    ("Fraps files", "*.Fraps"),
    ("Matroska files", "*.Matroska"),
    ("MPJPEG files", "*.MPJPEG"),
    ("MPEG-2(ES,MP3) files", "*.MPEG-2"),
    ("Ogg files", "*.OGG"),
    ("PVA files", "*.PVA"),
    ("QuickTime files", "*.QuickTime"),
    ("TS files", "*.TS"),
    ("WAV files", "*.WAV"),
    ("WebM files", "*.WebM"),
    ("avi files", "*.AVI"),
    ("mp4 files","*.mp4"),
    ))
    # print('creating and moving movie to new directory at: '+setdir(1))
    # movemovie()
    subs(root.filename)
    
def main():
    selectfile()
# print(getids('https://www.opensubtitles.org/en/search/sublanguageid-eng/idmovie-22566'))
# print(filename)
# getmoviesubs('spiderman')
# getsublink('https://www.opensubtitles.org/en/search/sublanguageid-eng/idmovie-22566')
# move_and_extract()
if __name__=='__main__':
    main()