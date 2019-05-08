import requests
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector

BASE_URL = "http://photon.bits-goa.ac.in/lms/login/index.php"
DOWNLOAD_URL = "http://photon.bits-goa.ac.in/lms/mod/folder/view.php?id=24349"
LOGIN_CREDS_FILE = open("credentials.txt", "r")

credentials = LOGIN_CREDS_FILE.read().strip().split("\n")
LOGIN_CREDS_FILE.close()
USERNAME = credentials[0]
PASSWORD = credentials[1]

s = requests.Session()
s.post(BASE_URL, data = {'username':USERNAME, 'password':PASSWORD} )
resp = s.get(DOWNLOAD_URL)
http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
encoding = html_encoding or http_encoding
soup = BeautifulSoup(resp.content, from_encoding=encoding)
counter = 0
for link in soup.find_all('a', href=True):
    download_link = (link['href'])
    if ".pdf" in download_link:
        counter += 1
        open('./files/' + str(counter) + ".pdf", 'wb').write(s.get(download_link).content)
