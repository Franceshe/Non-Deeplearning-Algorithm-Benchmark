import alice_in_wonderland
import re
from bs4 import BeautifulSoup

input_html = alice_in_wonderland.load_html()

def get_clean_html(target):
    soup = BeautifulSoup(target, 'html.parser')
    result = soup.prettify()
    return result

def extract_all_urls(link):
    for link in soup.find_all('a'):
        return link.get('href')

def extract_all_text():
    return soup.get_text()

def gettextonly(self, soup):
    v = soup.string
    if v == None:
        c = soup.contents
        resulttext = ''
        for t in c:
            subtext = str(self.gettextonly(t))
            resulttext += subtext + '\n'
            return resulttext
    else:
        return v.strip()

def separatewords(self, text):
    splitter = re.compile('\\W*')
    return [s.lower() for s in splitter.split(text) if s!='']


# Parse: html -> alltext>

# Testcase
test_clean = get_clean_html(input_html)
print("test_clean is")
print(test_clean)

soup = BeautifulSoup(input_html, 'html.parser')
parsed_html = soup.get_text()
print(soup.get_text())
splitter = re.compile('\\W*')
sep_words = [s.lower() for s in splitter.split(parsed_html) if s!='']
print(sep_words)

