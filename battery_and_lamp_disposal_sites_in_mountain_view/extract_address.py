import urllib2
import sys
data = urllib2.urlopen("http://www.mountainview.gov/depts/pw/recycling/hazard/default.asp")

for lines in data.readlines():
    sys.stdout.write(lines)