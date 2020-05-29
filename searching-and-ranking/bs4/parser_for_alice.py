import alice_in_wonderland
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

# Testcase
test_clean = get_clean_html(input_html)
print(test_clean)
