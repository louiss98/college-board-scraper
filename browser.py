from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from bs4 import BeautifulSoup
import time
from enum import Enum
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

from college import CollegeSearchResult
from college import Filters
import pandas as pd
import requests
import re
import openpyxl
from selenium import webdriver
from enum import Enum

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
def getSchools():
    driver_path = r"C:\Users\12035\edgedriver_win32\msedgedriver.exe"
    service = EdgeService(driver_path)
    options = EdgeOptions()
    options.add_argument("headless")
    driver = webdriver.Edge(service=service, options=options)

    # Programmatically set the filter and enter the collegeboard website programmatically.
    filter = Filters.SATascending.value

    # URL is the scrapers entry point into the domain. The url in question links to a search result page that displays colleges indexed by college board.
    entryURL = "https://bigfuture.collegeboard.org/college-search/filters?"
    modifiedURL = f"{entryURL}{filter}"
    driver.get(modifiedURL)

    # Wait for the element to be visible the timeout will be 10s, if 10s passes without the element terminate.
    wait = WebDriverWait(driver, 2)  # Adjust the timeout as needed
    element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.cs-college-card-outer-container')))

    # Access the html
    page_source = driver.page_source
    oup = BeautifulSoup(page_source, 'html.parser')

    loadMore(driver=driver)
    # loadMore()
    # loadMore()

    searchResults = []

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Parsing the search result webpage for relevant information
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
    return searchResults

# Loads additional colleges by pressing the load more button
def loadMore(driver):
    element = driver.find_element(By.CSS_SELECTOR, 'button.cb-btn.cb-btn-black.cb-btn-block')   # Identify the load more button
    driver.execute_script("arguments[0].scrollIntoView();", element)                            # Scrolls the element into view
    time.sleep(1)
    driver.execute_script("window.scrollBy(0, -275);")
    time.sleep(1)
    clickable_element = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'button.cb-btn.cb-btn-black.cb-btn-block'))
    )
    clickable_element.click()
    time.sleep(1)

# Configure the Selenium Browser
# def configureBrowser() -> WebDriver:
#     driver_path = r"C:\Users\12035\edgedriver_win32\msedgedriver.exe"
#     service = EdgeService(driver_path)
#     options = EdgeOptions()
#     options.add_argument("headless")
#     driver = webdriver.Edge(service=service, options=options)
#     return driver

# Crawls the profile page for the average net price
def tuitionCrawler(url):
    website = url + "/tuition-and-costs"
    college_name = url[44:len(website)]
    response = requests.get(
        url = website
    )
    if response.ok:
        soup = BeautifulSoup(response.content, 'html.parser')
        content_of_page = soup.find('main') 
        tuition_tag = content_of_page.find(class_= 'sc-f0cac891-3 bhdQaF cb-margin-bottom-16')
        return college_name, tuition_tag.text
    else:
        return 
    
# Generates an xlsx file
def toExcel(dataFrame):
    path = 'college_tuition.xlsx'
    dataFrame.to_excel(path, sheet_name = 'college_sheet')
    return
