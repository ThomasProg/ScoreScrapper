# pip install selenium
# sudo apt-get install -y chromium-browser
# pip install pdf2image

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import utils
import os
import requests
import time


advancedSearchUrl = 'https://www.mutopiaproject.org/advsearch.html'
# url = "https://www.mutopiaproject.org/cgibin/make-table.cgi?searchingfor=&Composer=&Instrument=Piano&Style=Classical&solo=1&timelength=1&timeunit=week&lilyversion="
url = "https://www.mutopiaproject.org/cgibin/make-table.cgi?startat=0&searchingfor=&Composer=&Instrument=&Style=&collection=beetson&id=&solo=&recent=&timelength=&timeunit=&lilyversion=&preview=0"
baseUrl = "https://www.mutopiaproject.org/cgibin/"

# Function to get the page content
def get_page_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed to retrieve page: {response.status_code}")
        return None


while(url != None):
	page_source = get_page_content(url)

	soup = BeautifulSoup(page_source, 'html.parser')

	# Extract spans with data-id attribute
	tables = soup.find_all('table', {"class":"table-bordered result-table"})
	for table in tables:
		# Find all tr elements within the tbody
		trs = list(table.children) # tr
		if (len(trs) < 4):
			continue

		tr = trs[3]

		tds = list(tr.children) # tr
		if (len(tds) < 4):
			continue

		td = tds[3]
		a = td.find("a")
		if (a == None):
			continue
		print("License: %s" % a.text)

		tdInf = tds[5]
		aInf = tdInf.find("a")
		assert(tdInf != None)
		assert(aInf.text == "More Information")
		link = aInf.get('href')
		print("More Information: %s" % (baseUrl + link))

		cell = list(trs[4].children)[3]
		a = cell.find("a")
		assert(a != None)
		midiLink = a.get('href')
		print("Midi file: ", midiLink)
		local_filename = utils.download_file(midiLink)

		print()

	a_tag = soup.find(lambda tag: tag.name == "a" and "Next 10" in tag.text)
	if (a_tag != None):
		next10Link = a_tag.get('href')
		url = baseUrl + next10Link
		print("New Page: %s" % url)
		# We're considerate of the server
		time.sleep(3)
	else:
		url = None

print("Download finished!")