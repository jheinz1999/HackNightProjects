import urllib2
import json
import sys
import re
from HTMLParser import HTMLParser
from collections import defaultdict
from collections import namedtuple
from xml.dom import minidom

def addresses_from_string_html(page):
    address = re.findall("</strong>[^<]+", page)
    for i in range(len(address)):
            address[i] = re.sub("</strong>", "", address[i])
    return address

def lat_lng_from_address(address):
    geom = json.load(urllib2.urlopen("http://maps.googleapis.com/maps/api/geocode/json?address="+urllib2.quote(address)))
    location = geom['results'][0]['geometry']['location']
    return (location['lat'], location['lng'])

class AddressExtractor(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.state = 'start'
        self.sections = []
        self.names_in_section = defaultdict(list)
        self.addresses_in_section = defaultdict(list)
        self.name_of_section = {
            'Paint': 'Paint',
            'Batteries ': 'Batteries & Lamps',
            'BATTERIES ONLY': 'Batteries Only',
        }

    def handle_starttag(self, tag, attrs):
        if tag == 'br':
            return
        if tag == 'strong':
            self.state = 'reading_name'
        elif tag == 'h1':
            self.state = 'reading_section'
        else:
            self.state = 'start'

    def handle_endtag(self, tag):
        if tag == 'br':
            return
        if tag == 'strong':
            self.state = 'reading_address'
        else:
            self.state = 'start'

    def handle_data(self, data):
        if self.state == 'reading_name':
            self.names_in_section[
                self.name_of_section[self.sections[-1]]].append(data.strip())
            self.state = 'start'
        elif self.state == 'reading_address':
            self.addresses_in_section[
                self.name_of_section[self.sections[-1]]].append(
                    data.strip() + ', Mountain View, CA')
            self.state = 'start'
        elif self.state == 'reading_section':
            self.sections.append(data)
            self.state = 'start'

data = urllib2.urlopen("http://www.mountainview.gov/depts/pw/recycling/hazard/default.asp")
page = data.read()
page = page[page.find("<h1>Paint</h1>"):page.find("<h1>MEDICATION")]

extractor = AddressExtractor()
extractor.feed(page)

Location = namedtuple('Location', 'name address')
locations_in_section = {}
for key in extractor.addresses_in_section:
    locations_in_section[key] = [Location(n, a) for n, a in
        zip(
            extractor.names_in_section[key],
            extractor.addresses_in_section[key])]

Placemark = namedtuple('Placemark', 'name address lat lng')
placemarks_in_section = {}
for section in locations_in_section:
    placemarks_in_section[section] = [
        Placemark(n, a, lat, lng) for (n, a), (lat, lng) in zip(
            locations_in_section[section],
            [lat_lng_from_address(l.address) for l in (
                locations_in_section[section])])]

kmlDoc = minidom.Document()
docElement = kmlDoc.createElement('Document')
kmlDoc.appendChild(docElement)
for section in placemarks_in_section:
    folder = kmlDoc.createElement('Folder')
    docElement.appendChild(folder)
    folderName = kmlDoc.createElement('name')
    folder.appendChild(folderName)
    folderName.appendChild(kmlDoc.createTextNode(section))

    for placemark in placemarks_in_section[section]:
        placemarkElement = kmlDoc.createElement('Placemark')
        folder.appendChild(placemarkElement)

        name = kmlDoc.createElement('name')
        name.appendChild(kmlDoc.createTextNode(placemark.name))
        placemarkElement.appendChild(name)

        address = kmlDoc.createElement('address')
        address.appendChild(kmlDoc.createTextNode(placemark.address))
        placemarkElement.appendChild(address)

        coordinates = kmlDoc.createElement('coordinates')
        coordinates.appendChild(
            kmlDoc.createTextNode('{},{}'.format(placemark.lat, placemark.lng)))
        placemarkElement.appendChild(coordinates)

sys.stdout.write(kmlDoc.toprettyxml(' '))
