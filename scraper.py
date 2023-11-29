from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from bs4 import BeautifulSoup
import time

# URL is our entry point to the domain we want to scrape. The url in question links to a search result page that contains all colleges listed on college board.

url = "https://bigfuture.collegeboard.org/college-search/filters"
driver_path = r"C:\Users\12035\edgedriver_win32\msedgedriver.exe"

service = EdgeService(driver_path)
options = EdgeOptions()
driver = webdriver.Edge(service=service, options=options)

# Navigate to the URL
driver.get(url)

# Wait for the page to load will fix later. (hold until element is present)
time.sleep(3)

# Access the source html
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# Search for all card elements. we need to do this more efficiently. cannot continuely search all will have revisited elements
links = soup.find_all('a', class_='cs-college-card-college-name-link')

# Print the 'href' attribute for each link
for link in links:
    href = link.get('href')
    print(href)

time.sleep(5)