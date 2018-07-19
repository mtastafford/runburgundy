import codecs
from bs4 import BeautifulSoup
from html.parser import HTMLParser

f = codecs.open('index.html','r')
#print(f.read())
soup = BeautifulSoup(f, 'html5lib')
#print(soup.prettify())
#print(soup.title)
#print(soup.p)
#print(soup.find_all('section'))
leaders = soup.section.div

#print(leaders)

print(leaders)
#print(soup.get_text())
