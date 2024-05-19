#!/usr/bin/env python
# coding: utf-8

# # Linkedin Jobs - Web Scraping


from selenium import webdriver
import time
import pandas as pd
import os

from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

url1 = 'https://www.linkedin.com/jobs/search/?currentJobId=3919096655&geoId=105214831&keywords=marketing%20data%20analyst&location=Bengaluru%2C%20Karnataka%2C%20India&origin=JOB_SEARCH_PAGE_LOCATION_AUTOCOMPLETE&refresh=true'

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Initialize Chrome options
chrome_options = Options()

# Uncomment the following line to open Chrome in headless mode (without UI)
# chrome_options.add_argument("--headless")

# Initialize ChromeDriver with options
driver = webdriver.Chrome(options=chrome_options)

driver.get(url1)
driver.implicitly_wait(10)

a = True
i=0

while (a):
    try: 
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)  # Decreased wait time for scrolling animation
    
        # Find the button element
        button = driver.find_element(By.XPATH, '//*[@id="main-content"]/section[2]/button')
    
        # Scroll to the button element
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        time.sleep(0.5)  # Decreased wait time for scrolling animation

        driver.execute_script("arguments[0].click();", button)
        time.sleep(0.1) 
        
        if not button.is_displayed():
            pass
        else:
            i+=1
        if i>0:
            if not button.is_displayed():
                a = False
                
    except Exception as e:
        print("Exception occurred:", e)
        pass

time.sleep(0.1)

n = driver.find_elements(By.XPATH, '//*[@id="main-content"]/section[2]/ul/li')
x = len(n)
x

companyname = []
titlename = []
dateposted = []

for j in range(x):
    company = driver.find_elements(By.CLASS_NAME, 'base-search-card__subtitle')[j].text
    companyname.append(company)
    
    title = driver.find_elements(By.CLASS_NAME, 'base-search-card__title')[j].text
    titlename.append(title)

#print("companyname - ", companyname, "\n")
#print("\n", "titlename - ", titlename)

listoflinks = []
findlink = driver.find_elements(By.CLASS_NAME, 'base-card__full-link')

for k in findlink:
    listoflinks.append(k.get_attribute('href'))
    
datetime = []
dates = driver.find_elements(By.CLASS_NAME, 'job-search-card__listdate')

for p in dates:
    datetime.append(p.get_attribute('datetime'))
#print("\n", "date posted - ", datetime)


companyfinal = pd.DataFrame(companyname, columns=["company"])
titlefinal = pd.DataFrame(titlename, columns=["title"])

final = companyfinal.join(titlefinal)

finallinks = pd.DataFrame(listoflinks, columns=["links"])

output_old = final.join(finallinks)

datesposted = pd.DataFrame(datetime, columns=["posting_date"])

output = output_old.join(datesposted)
output


# # Exploratory Data Analysis

output.to_csv("linkedinjobsoutput.csv")

import seaborn as sns
import matplotlib.pyplot as plt

output.info()
output.describe()
output.isnull().sum()
output.nunique()
output.sort_values(by="posting_date",ascending=False).head()


# Display value counts for categorical variables
categorical_cols = output.select_dtypes(exclude='number').columns
for col in categorical_cols:
    print(f"\nValue Counts for {col}:")
    print(output[col].value_counts())


# # DATA VISUALIZATION

# Get the top 10 hiring companies
top_hiring_companies = output['company'].value_counts().head(10)

# Plot top hiring companies
plt.figure(figsize=(12, 8))
sns.barplot(x=top_hiring_companies.index, y=top_hiring_companies.values, palette='Set2')
plt.title('Top Hiring Companies')
plt.xlabel('Company')
plt.ylabel('Number of Job Postings')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

start_date = '2024-04-18'
end_date = '2024-04-30'

# Filter the data for the specified date range
filtered_output = output[(output['posting_date'] >= start_date) & (output['posting_date'] <= end_date)]

# Get the frequency of each company
company_counts = filtered_output['company'].value_counts()

# Sort companies based on frequency
sorted_companies = company_counts.index.tolist()

# Create the plot
plt.figure(figsize=(12, 8))
sns.countplot(data=filtered_output, x='company', palette='Set2', order=sorted_companies)
plt.title('Distribution of dates across companies (Apr 2024)')
plt.xlabel('Company Name')
plt.ylabel('Frequency')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()



# Define the job titles you want to include in the pie chart
selected_titles = ['Business Finance Analyst', 'Business Data Analyst', 'Marketing Analyst', 'Business Advisory Analyst']

# Filter the data to include only the selected job titles
filtered_output = output[output['title'].isin(selected_titles)]

# Get the frequency of each selected job title
title_counts = filtered_output['title'].value_counts()

# Plotting
plt.figure(figsize=(10, 8))
plt.pie(title_counts, labels=title_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Distribution of Selected Job Titles')
plt.axis('equal') 
plt.show()


# Calculate length of job descriptions
output['title'] = output['title'].apply(len)

# Plot distribution of description lengths
plt.figure(figsize=(12, 8))
sns.histplot(data=output, x='title', bins=30, kde=True, color='skyblue')
plt.title('Distribution of Job Description Lengths')
plt.xlabel('Description Length')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

#This analysis can help in understanding the level of detail typically provided in job descriptions, 
#identifying potential patterns or outliers, and informing decisions related to job posting content 
#or candidate expectations

