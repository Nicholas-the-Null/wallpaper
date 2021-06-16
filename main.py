import re
import os
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
from tqdm import tqdm
from PIL import Image
from io import BytesIO
import hashlib
def is_valid_url(url):
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)


while True:
    site=input("give me the site for download picture:")
    if is_valid_url(site) is not None:
        if str(requests.get(site))=="<Response [200]>":
            break
        else:
            print("site offline")
    else:
        print("non è un link")

while True:
    path=input("select a path or digit ?path for create a new one or ++ for use current dir:")
    if path=="++":
        path=os.getcwd()
        break
    elif path[0]=="?":
        try:
            os.mkdir(path[1:len(path)])
            break
        except OSError:
            print("error path name not valid")
    else:
        if os.path.exists(path) and os.path.isdir(path):
            break
        else:
            print("error")

def get_all_images(url):
    """
    Returns all image URLs on a single `url`
    """
    soup = bs(requests.get(url).content, "html.parser")
    urls = []
    for img in tqdm(soup.find_all("img"), "Extracting images"):
        img_url = img.attrs.get("src")
        if not img_url:
            # if img does not contain src attribute, just skip
            continue
        # make the URL absolute by joining domain with the URL that is just extracted
        img_url = urljoin(url, img_url)
        # remove URLs like '/hsts-pixel.gif?c=3.2.5'
        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass
        # finally, if the url is valid
        if is_valid_url(img_url):
            urls.append(img_url)
    return urls


lista=get_all_images(site)

lista_down=[]

for url in lista:
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    if img._size[0] >= 300 and img._size[1] >= 300: #altezza[0] largezza[1]
        download=True
    else:
        download=False
    if download==True:
        filename = os.path.join(path, url.split("/")[-1])
        r = requests.get(url, allow_redirects=True)
        open(filename, 'wb').write(r.content)
        lista_down.append(filename)
        

hash_file=[]
delete_file=[]
            
for x in lista_down:
    md5 = hashlib.md5()
    with open(x, "rb") as thefile:
        buf = thefile.read()
        md5.update(buf)
    sha=md5.hexdigest()
    if sha in hash_file:
        delete_file.append(x)

for x in delete_file:
    try:
        os.remove(x)
    except Exception:
        pass




input("finito")