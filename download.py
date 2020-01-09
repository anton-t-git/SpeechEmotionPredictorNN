from tqdm import tqdm
from lxml import html
import requests
import urllib.request
import re
import time
import os.path

HANDLE = '^/handle/[0-9]+/[0-9]+$'
BASE_URL = 'https://tspace.library.utoronto.ca'
DATASET_DIR = './data/'

if not os.path.isdir(DATASET_DIR):
    os.mkdir(DATASET_DIR)

page = requests.get(BASE_URL + '/handle/1807/24487')
tree = html.fromstring(page.content)
subset = [ href.attrib['href'] for href in tree.xpath('//a') if re.match(HANDLE, href.attrib['href'])]

for s in subset:
    print(s)
    wav_page = requests.get(BASE_URL + s)
    tree = html.fromstring(wav_page.content)
    links = [href.attrib['href'] for href in tree.xpath('//a') if 'wav' in href.attrib['href']]
    for link in tqdm(links):
        local = link.split('/')[-1]
        if not os.path.isfile('' + local):
            try:
                urllib.request.urlretrieve(BASE_URL + link, 'data/' + local)
                #print('Download: ', link)
            except IOError:
                print('Err: ', link)
            time.sleep(1)
        else:
            print('Already Exists: ', link)
