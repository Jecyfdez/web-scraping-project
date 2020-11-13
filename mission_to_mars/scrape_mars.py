#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install webdriver_manager')
get_ipython().system('pip install splinter')


# ## Step 1 - Scraping

# In[2]:


# Dependencies
import os
from bs4 import BeautifulSoup
import requests
import pymongo
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


# ### NASA Mars News

# In[3]:


# Setup splinter
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # In[4]:

def scrape():
    # Mars News Titles
    browser = init_browser()
    mars_collection = {}
    
    # URL of page to be scraped
    url_news = 'https://mars.nasa.gov/news/'

    # Retrieve page with the requests module
    response = requests.get(url_news)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')


    # In[5]:


    # pull titles and body from website
    results = soup.find_all('div', class_="slide")
    for result in results:
        titles = result.find('div', class_="content_title")
        title = titles.find('a').text
        bodies = result.find('div', class_="rollover_description")
        body = bodies.find('div', class_="rollover_description_inner").text
    print('----------------')
    print(title)
    print(body)


    # ### JPL Mars Space Images - Featured Image

    # In[6]:


    # URL of page to be scraped
    url_img = ('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')

    # Retrieve page with the requests module
    response = requests.get(url_img)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')


    # In[7]:


    # pull images from website
    images = soup.find_all('a', class_="fancybox")
    print(images)


    # In[8]:


    # pull image link
    src = []
    for image in images:
        pic = image['data-fancybox-href']
        src.append(pic)

    featured_image_url = 'https://www.jpl.nasa.gov' + pic
    featured_image_url


    # ### Mars Facts

    # In[10]:


    mars_facts_url = "https://space-facts.com/mars/"
    table = pd.read_html(mars_facts_url)
    table


    # In[11]:


    df=table[0]
    df.columns = ["Description", "Data"]
    df.set_index(["Description"])


    # In[12]:


    html_table = df.to_html(index=False)
    html_table.replace('\n','')
    df.to_html('table.html')


    # In[13]:


    get_ipython().system('open table.html')


    # ### Mars Hemispheres

    # In[14]:


    url_hem = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url_hem)

    import time
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_hemisphere=[]


    # In[15]:


    # loop through the four tags and load the data to the dictionary

    for i in range (4):
        time.sleep(5)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        partial = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary={"title":img_title,"img_url":img_url}
        mars_hemisphere.append(dictionary)
        browser.back()


    # In[16]:


    print(mars_hemisphere)
    return mars_collection


    # ## Step 2 - MongoDB and Flask Application

    #
