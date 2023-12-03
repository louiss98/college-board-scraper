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
from college import Filters
import pandas as pd
import requests
import re
import openpyxl
from selenium import webdriver
from browser import getSchools
from browser import toExcel
from browser import tuitionCrawler

searchResults = getSchools()

tuition = []
schoolNames = []

for result in searchResults:
    sub = "https://bigfuture.collegeboard.org/colleges/"
    if result.href.find(sub) != -1:
        college = tuitionCrawler(result.href)
        schoolNames.append(college[0])
        tuition.append(college[1])
        print(result.href)

data = {'School Names' : schoolNames,
        'Tuition': tuition
        }

df = pd.DataFrame(data)
toExcel(df)