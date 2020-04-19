import sys
import requests
import bs4
import time
import platform
import shutil
import os
from zipfile import ZipFile
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from selenium import webdriver
import urllib.request 
import urllib
import hashlib

def get_hash(name):
    readsize = 64 * 1024
    with open(name, 'rb') as f:
        size = os.path.getsize(name)
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()

def getsubs(path_to_mov):
    user_agent = 'SubDB/1.0 (easysubs/0.1; https://github.com/leonkoech/easysubs)'
    movie_path = path_to_mov
    moviename = os.path.join(os.getcwd(), movie_path)
    language = 'en'
    action = 'download'
    base_url = 'http://api.thesubdb.com/?'
    hashed = get_hash(moviename)

    content = {
        'action': action,
        'hash': hashed,
        'language': language,
    }

    url = base_url + urllib.parse.urlencode(content)
    req = urllib.request.Request(url)
    req.add_header('User-Agent', user_agent)
    res = urllib.request.urlopen(req)
    subtitles = res.read()

    index = moviename.rfind('.')
    file_name = moviename[0:index] + '.srt'
    with open(file_name, 'w') as f:
        f.write(subtitles)
    print ("Downloaded!")
def tupletostring(ins):
    string=''
    for b in ins:
        string+=b
    return string
def movemovie():
    # create movie directory first then move
    os.makedirs(setdir(2))
    os.rename(selectfile.sfdir,setdir(1))
    print('movie has been moved to new directory at'+setdir(2))
def splitdir():
    old_string=selectfile.sfdir
    old_string=old_string.replace(' ','-')
    k = old_string.rfind("/")
    new_string = old_string[:k] + " " + old_string[k+1:]
    return new_string
def getdir():
    new_string=splitdir().split()
    new_string.pop(-1)
    new_string= tupletostring(new_string).replace('-',' ')
    return new_string
def setdir(r):
    if r==1:
        newdir=getdir()+'/'+getname()+'/'+getname_ext()
    elif r==2:
        newdir=getdir()+'/'+getname()+'/'
    return newdir
def getname_ext():
    movieext=splitdir().split()
    movieext.pop(0)
    movieext= tupletostring(movieext).replace('-',' ')
    return movieext
def getname():
    #returns name of movie without extension
    new_string=splitdir().split()
    new_string.pop(0)
    new_string=tupletostring(new_string)
    new_string=new_string.replace('.',' ')
    new_string=new_string.split()
    new_string.pop(-1)
    new_string=tupletostring(new_string)
    new_string=new_string.replace('-',' ')
    return new_string
def delete_miscallenelous(dontdelete):
    # this function takes in an array of elements that you should not delete
    os.chdir('/home/keonssss/mtr/spiderman/spiderman')
    files=os.listdir()
    print(files)
    res = [ ele for ele in files ] 
    for a in dontdelete: 
        if a in files: 
            res.remove(a)
    print(res)
    for element in res:
        try:
            os.remove(element)
            print('residue files deleted')
        except:
            print('no residue files found.')

def selectfile():
    #this method presents the user with  gui to select the movie file
    Tk().withdraw() 

    filename = askopenfilename(initialdir = "/home/keonssss/mtr",title = "Select movie file",filetypes = (
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
    selectfile.sfdir=filename
    print('creating and moving movie to new directory at: '+setdir(1))
    movemovie()
    print('searching and downloading subs...')
    getsubs(setdir(2))
    
# other_os_open()
# print(get_movie_name("/home/keonssss/python/Automation Projects/easymovie/a really long movie name.mp4"))
def getids(weburl):
    content = requests.get(weburl).text # Get page content
    soup = bs4.BeautifulSoup(content, 'lxml')
    tablebody = soup.find('tbody')
    itemname=tablebody.find_all('tr')
    myarr=[]
    for item in itemname:
        itemid=item.get('id')
        if itemid!=None:
            itemid=itemid.replace('name','main')
            myarr.append(itemid)
       
    return myarr[0]
def getsublink(url):
    content = requests.get(url).text # Get page content
    soup = bs4.BeautifulSoup(content, 'lxml')
    item = soup.find(id=getids(url))
    itemlink=item.find('a')
    print(itemlink)
def extractsub(moviename,moviedir):
    #list files in current directory
    os.chdir(moviedir)
    files =os.listdir()
    print(files)
    files.remove(moviename)
    print(files)
    subzip=tupletostring(files)
    with ZipFile(subzip, 'r') as zipObj:
    # Extract all the contents of zip file in current directory
        print('extracting zip...')
        zipObj.extractall()
        extractedfiles=os.listdir()
        for sub in extractedfiles:
            #exclude the movie
            if sub != moviename:
                sub=sub.replace('.',' ')
                sub=sub.split()
                extension=sub[-1]
                if extension== 'ssf' or extension=='srt' or extension=='ssa' or extension=='svcd' or extension=='usf' or extension=='idx' or extension== 'mpl' or extension=='txt' or extension=='pjs' or extension=='psb' or extension=='rt' or extension=='smi' or extension== 'aqt' or extension=='cvd' or extension=='dks' or extension=='jss' or extension=='sub' or extension=='ttxt':
                    sub.pop(-1)
                    subs=''
                    for b in sub:
                        subs+=b+' '
                    subs=subs.rstrip()
                    subs=subs.replace(' ','.')
                    #change movie name to name without extension
                    moviename=moviename.replace('.',' ')
                    moviename=moviename.split()
                    moviename.pop(-1)
                    mvn=''
                    for b in moviename:
                        mvn+=b+' '
                    mvn=mvn.rstrip()
                    #now replace that string
                    os.rename(subs+'.'+extension,mvn+'.'+extension)
                    #now delete the zip file
                    os.remove(subzip)
                    #delete anything that is not the movie
                    delete_miscallenelous([getname_ext,mvn+'.'+extension])
                    print('🎉🎉 easymovie has downloaded your subtitle 🎉🎉')
                elif extension=='nfo' or extension=='zip':
                    pass
                else:
                    print('this subtitle format is not supported. Easysubs uses subtitile files supported by vlc.')
        
def searchsubs(moviename,moviedir):
        downloaddir="download.default_directory="+moviedir
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--test-type")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument('--window-size=1420,1080')
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument(downloaddir)
        options.binary_location = "/usr/bin/google-chrome"
        prefs = {'download.default_directory' : moviedir}
        options.add_experimental_option('prefs', prefs)
    
        driver = webdriver.Chrome(options=options, executable_path='/usr/local/bin/chromedriver')
        driver.get('https://www.opensubtitles.org/en/search/sublanguageid-eng')
        time.sleep(5)
        searchInput=driver.find_element_by_xpath('//*[@id="search_text"]')
        searchInput.send_keys(moviename)
        time.sleep(3)
        searchbutton=driver.find_element_by_xpath('//*[@id="search_submit"]')
        searchbutton.click()
        time.sleep(5)
        # click the first movie link
        movielink =driver.find_element_by_xpath('//*[@id="'+getids(driver.current_url)+'"]/strong/a')
        print('1. clicking button with id = '+getids(driver.current_url))
        movielink.click()
        time.sleep(4)
        # click the second movie link
   
        getsubs =driver.find_element_by_xpath('//*[@id="'+getids(driver.current_url)+'"]/strong/a')
        print('2. clicking button with id = '+getids(driver.current_url))
        getsubs.click()
        time.sleep(3)
        downloadbtn = driver.find_element_by_xpath('//*[@id="bt-dwl-bt"]')
        window_before = driver.window_handles[0]
        downloadbtn.click()
        time.sleep(3)
        driver.switch_to.window(window_before)
        # driver.close()

        time.sleep(15)
        print('sub has been downloaded to:'+ moviedir)
        driver.quit()
        time.sleep(3)
def main():
    selectfile()
# print(getids('https://www.opensubtitles.org/en/search/sublanguageid-eng/idmovie-22566'))
# print(filename)
# getmoviesubs('spiderman')
# getsublink('https://www.opensubtitles.org/en/search/sublanguageid-eng/idmovie-22566')
# move_and_extract()
if __name__=='__main__':
    main()