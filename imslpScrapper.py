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

url = 'https://imslp.org/wiki/Special:IMSLPImageHandler/62144'  # Replace with your target URL

driver = webdriver.Chrome()
driver.get(url)


page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')
link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "I understand")))
link.click()

# Wait until the page is fully loaded (adjust timeout as needed)
WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.TAG_NAME, "span")))

# Once loaded, get the page source and pass it to BeautifulSoup
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# Extract spans with data-id attribute
spans_with_data_id = soup.find_all('span')
for span in spans_with_data_id:
    if (span.has_attr('data-id')):
        dataid = span["data-id"]
        if (dataid.endswith(".pdf")):
            directory = "downloads"
            local_filename = os.path.join(directory, dataid.split('/')[-1])
            utils.download_file(dataid, directory)
            print("Downloaded %s" % dataid)

            output = os.path.join(directory, "pngs")
            utils.pdf_to_png(local_filename, output)


# Close the WebDriver
driver.quit()
