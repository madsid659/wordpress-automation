import os
from os import path
from urllib.request import urlopen
from bs4 import BeautifulSoup
import subprocess
from pythonping import ping
from tqdm import tqdm
import requests
import gzip
import shutil
import tarfile

wp = 'wordpress.tar.gz'
file_dst="/var/www/html"
mkdir_command= "sudo mkdir -p "+file_dst
cwd = os.getcwd()


def check_root_privilliage():
    uid = os.getuid()
    if uid != 0:
        print("exiting script, You dont have root privilege")
        exit()


def check_internet():
    if ping("8.8.8.8"):
        print("internet working fine")
    else:
        print("you dont have a working internet connection, Exiting script.")
        exit(10)


def download_wordpress(fname):
    url = "https://wordpress.org/download/"
    try:
        page = urlopen(url)
    except:
        print("Error opening the URL")
    soup = BeautifulSoup(page, 'html.parser')
    content = soup.find('div', {"class": "call-to-action col-12"})
    links = []
    for link in content.findAll('a'):
        links.append(link.get('href'))
    resp = requests.get(links[1], stream=True)
    total = int(resp.headers.get('content-length', 0))
    with open(fname, 'wb') as file, tqdm(
            desc=fname,
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)


def unzip_wordpress():
    file = tarfile.open('wordpress.tar.gz')

    if path.exists("file_dst"):
        print("path ",file_dst,"exist")
    else:
        # os.mkdir("file_dst")
        subprocess.call(mkdir_command, shell=True)
    file.extractall(file_dst)
    file.close()


check_root_privilliage()
print("continue script")
# check_internet()
download_wordpress(wp)
unzip_wordpress()
print(mkdir_command)

