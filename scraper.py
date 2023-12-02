from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from bs4 import BeautifulSoup
import time
from enum import Enum
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from college import CollegeSearchResult

class Filters(Enum):
    HighestGraduationRate = 'sortBy=gradRate'
    SATascending = 'sortBy=satAsc'
    SATdescending = 'sortBy=satDes'
    Alphabetical = 'sortBy=name'
    ReachMathSafety = 'sortBy=rms'
    Default = 'sortBy=default'

# Configure the Selenium Browser
driver_path = r"C:\Users\12035\edgedriver_win32\msedgedriver.exe"
service = EdgeService(driver_path)
options = EdgeOptions()
driver = webdriver.Edge(service=service, options=options)

# Programmatically set the filter
filter = Filters.HighestGraduationRate.value

# URL is the scrapers entry point into the domain. The url in question links to a search result page that displays colleges indexed by college board.
entryURL = "https://bigfuture.collegeboard.org/college-search/filters?"
modifiedURL = f"{entryURL}{filter}"
driver.get(modifiedURL)

# Wait for the element to be visible the timeout will be 10s, if 10s passes without the element terminate.
wait = WebDriverWait(driver, 3)  # Adjust the timeout as needed
element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.cs-college-card-outer-container')))

# Access the html
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

'''
The relevant element we are looking for is the card element that houses the information we wish to scrape. 
However the element is composed of other elements as well and the information is spread out amongst those elements. Below is a simplified subtree for the container element.

cs-college-card-outer-container -> (the base)
    ...
    cs-college-card-college-name-link cb-roboto-medium cb-black1-color-> (where the href is stored)
        ...
            ...
                cs-college-card-college-name cb-roboto-medium -> (where name's stored)
                    ...
                    cs-college-card-college-address  cb-roboto-light cb-paragraph1-st cb-padding-top-8 -> (where the locations stored)
        ...
'''

searchResults = []

containers = soup.find_all(class_='cs-college-card-outer-container')

for container in containers:
    # The relevant information needed to build a CollegeSearchResult is located in multiple subelements that need to be search for accordingly.
    hrefElement = container.find(class_='cs-college-card-college-name-link cb-roboto-medium cb-black1-color')
    href = hrefElement.get('href')

    nameElement = container.find(class_='cs-college-card-college-name-link-text')
    name = nameElement.text

    adddressElement = container.find(class_='cs-college-card-college-address')
    address = adddressElement.text

    characteristicsElement = container.find(class_='cs-college-card-details-profile-inline-list cb-text-list cs-college-card-details-profile-info-text')
    characteristics = characteristicsElement.text

    '''
    Details
    The detail/profile elements in the container are defined using the same class name (cb-no-padding cs-college-card-details-profile-info-text). 
    Therefore we have to search by their 'datatestid' an attribute that represents a psudoname likely created by the collegeboard devs to distinguish between the elements when accessing or debugging the html.
    '''

    graduationElement = container.find(attrs={"data-testid": "cs-college-card-details-profile-school-graduation-rate"})
    graduation = graduationElement.text

    apyElement = container.find(attrs={"data-testid": "cs-college-card-details-profile-school-average-cost"})
    apy = apyElement.text

    satElement = container.find(attrs={"data-testid": "cs-college-card-details-profile-school-sat-range"})
    sat = satElement.text

    searchResult = CollegeSearchResult(
        name = name,
        location = address,
        characteristics = characteristics,
        graduation_rate = graduation,
        apy = apy,
        sat = sat,
        href= href
    )

    searchResults.append(searchResult)
    
print(searchResults[0])

time.sleep(10)