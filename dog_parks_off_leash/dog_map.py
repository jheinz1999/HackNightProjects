from bs4 import BeautifulSoup
import urllib2 as ul

data = ul.urlopen('http://www.mountainview.gov/depts/cs/parks/parks/dog.asp')

with open('dog_website_mountainview.html', 'w') as file:
	file.write('test')

print file.closed
	