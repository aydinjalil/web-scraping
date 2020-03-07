#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pandas as pd


# # 1. NASA Mars News
# 
# ## Beware: Please put your own path to chromedriver.exe

# In[2]:


def init_browser():
    """This function open the Google Chrome browser when called"""
    
    executable_path = {"executable_path": "C:/Users/aydin/Downloads/chromedriver_win32/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


# In[3]:


def scrape_nasa():
    
    """The function returns title and paragraph text of the latest news on NASA website"""
    
# Create lists for title and paragpraph.
    titles = []
    para = []
    
    browser = init_browser()
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    
# Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    for title in soup.find_all('div', class_='content_title'):
        if title.a:
            titles.append(title.a.text)
    for paragraph in soup.find_all('div', class_='article_teaser_body'):
        para.append(paragraph.text)
    print(f"Number of titles: {len(titles)}\nNumber of Paragraphs: {len(para)}\n")

    print(f"\033[1m{titles[0]}:\033[0m\n{para[0]}")

    latest_title = titles[0]
    latest_para = para[0]
    browser.quit()
    return latest_title, latest_para


# We can see that titles are greater in number than the paragraph texts. Since the assignment asks to fetch only the first title and associated text we just have to visually verify whether both elements are what we are looking for.  

# # 2. JPL Mars Space Images - Featured Image
# 
# ### Small function to fetch the largesize image

# In[4]:


def scrape_image():
    """The function returns the url of a largesize Mars picture"""

#Create a list and an empty string to store image urls and the each url
    high_res_pics = []
    image_url = ''
    
    browser = init_browser()
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    for anchors in soup.find_all('a', class_='fancybox'):
        if 'largesize' in anchors['data-fancybox-href']:
            image_url = 'jpl.nasa.gov' + anchors['data-fancybox-href']
            high_res_pics.append(image_url)
    featured_image_url = high_res_pics[0]
    browser.quit()
    return featured_image_url


# # 3. Mars Weather - Scraping Twitter
# 
# * For some reason splinter did not work while trying to fetch the weather information from twitter. It kept delivering the Login and Sign in pages. So I needed to go back to requests the url.
# 
# 
# ## Small function to scrape the weather data from Twitter

# In[5]:


def scrape_weather():
    """This function returns the latest Mars weather stats"""
    
    # list to store all available weather information. We will pick the latest one by simply saying weather_list[0]
    weather_list = []
    
    url = "https://twitter.com/marswxreport?lang=en" 
    html = requests.get(url).text
    html = html.replace("\n", ", ")
    soup = BeautifulSoup(html, 'html.parser')
    
    # Scrape the website
    
    for weather in soup.find_all('div', class_= "js-tweet-text-container"):
        if "InSight" in weather.p.text:
            weather_list.append(weather.p.getText().split('InSight')[1])

    #latest Mars Weather stats
    mars_weather = weather_list[0].split('pic.twitter.com')[0]
    return mars_weather


# In[6]:


scrape_weather()


# # 4. Mars Facts - Web scraping with Pandas and BeautifulSoup
# 
# ## Small function to scrape information from table

# In[7]:


def mars_facts():
    """This function scrapes the information about Mars and returns it in html format"""
    
    url = "https://space-facts.com/mars/" 
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')
    table = soup.find_all('table')[0] 
    df = pd.read_html(str(table))
    mars_html_table = df[0].to_html()
    return mars_html_table


# # 5. Mars Hemispheres

# In[8]:


def img_getter(titles, url_list):
    """This function scrapes the urls passed in url_list and fetches title and img_url, puts it into dictionary and returns list of dinctionaries"""
    
    hemisphere_data = []
    hemisphere={}
    for i in range(len(titles)):
        response = requests.get(url_list[i])
        hemisphere_soup = BeautifulSoup(response.content, 'html.parser')
        
        for download in hemisphere_soup.find_all('div', {'class':'downloads'}):
            hemisphere['title'] = titles[i]
            hemisphere['img_url'] = download.ul.li.a['href']
        
        hemisphere_data.append(dict(hemisphere))
        
    return hemisphere_data


# ## Small function to get images from Astropedia 

# In[9]:


def hemispheres():
    """This function returns the images of the Mars Hemispheres. Calls function image_getter to obtain the urls"""
    
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')
    
    
    hemisphere_urls  = []
    title_list = []
    for items in soup.find_all('div', class_='item'):
        title = items.div.h3.text.replace(' Enhanced', '')
    
    # Create urls by concatenating the start and the portion of url derived from href
    
        hemisphere_urls.append(url.split('search')[0] + items.a['href'])
        title_list.append(title)

    # Call image_getter
    
    hemisphere_image_urls = img_getter(title_list, hemisphere_urls)
    return hemisphere_image_urls


# In[ ]:




