import urllib2
import sys
import re
data = urllib2.urlopen("http://www.mountainview.gov/depts/pw/recycling/hazard/default.asp")
page = data.read()
page = page[page.find("Batteries &amp; Lamps"):page.find("BATTERIES ONLY")]
address = re.findall("</strong>[^<]+", page)
for element in address:
	print re.sub("</strong>", "", element)